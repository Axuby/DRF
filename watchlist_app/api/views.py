from typing import List
from watchlist_app.api.throttlings import ReviewCreateThrottle, ReviewListThrottle
from watchlist_app.models import Review, StreamPlatform, WatchList
from watchlist_app.api.serializers import ReviewSerializer, StreamPlatformSerializer, WatchListSerializer
from logging import StreamHandler
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework import status
from rest_framework.viewsets import ViewSet, ModelViewSet, ReadOnlyModelViewSet
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin
from rest_framework.generics import (GenericAPIView,
                                     ListCreateAPIView,
                                     ListAPIView,
                                     CreateAPIView,
                                     RetrieveUpdateDestroyAPIView,
                                     RetrieveUpdateAPIView)
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .permissions import IsReviewUserOrReadOnly, IsAdminOrReadOnly
from .paginations import WatchListPagination
# Create your views here.


class SearchReviewFromUser(ListAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["review_user__username",
                        "description", "rating", "is_active"]


class SearchWatchList(ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    pagination_class = WatchListPagination
    filter_backends = [OrderingFilter]

    ordering_fields = ["avg_rating", "title", ]
    # filter_backends = [SearchFilter]
    # search_fields = ["^title", "storyline", ]
    # filter_backends = [DjangoFilterBackend] must set the fields to values!
    # filterset_fields = ["title", "storyline", ]

    # def get_queryset(self):
    #     query = super().get_queryset()
    #     username = self.request.query_params.get("username", None)
    #     print(username)
    #     print(query)
    #     if username is not None:
    #         query = query.filter(
    #             review_user__username=username)
    #         print(query)
    #         return query
    #     return {"Error": "Error"}


class ReviewFromUser(ListAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        users = super().get_queryset()
        query = users.filter(
            review_user__username=self.kwargs.get("username", None))
        print(query)
        return query
    # def get_queryset(self):
    #     users = super().get_queryset()
    #     keyword = self.kwargs.get("keyword", None)
    #     query = users.filter(Q(review_user__icontains=keyword) | Q
    #                           (description__icontains=keyword))
    #     print(query)

    #     return query


class ReviewCreate(CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    throttle_classes = [ReviewCreateThrottle]

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        movie = get_object_or_404(WatchList, pk=self.kwargs.get('pk', None))
        review_user = self.request.user

        review = Review.objects.filter(
            review_user=review_user, watchlist=movie)

        if review.exists():
            raise ValidationError("You have already reviewed this movie!")
        if movie.number_of_ratings == 0:
            movie.avg_rating = serializer.validated_data.get("rating")
        else:
            movie.avg_rating = (movie.avg_rating +
                                serializer.validated_data.get("rating"))/2
        movie.number_of_ratings = movie.number_of_ratings + 1

        serializer.save(watchlist=movie,
                        review_user=review_user)
        print(serializer)
        print(serializer.data)
        # return super().perform_create(serializer)


class ReviewList(ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewListThrottle]

    def get_queryset(self):
        # stream = get_object_or_404(
        #     StreamPlatform, watchlist=self.kwargs.get('pk', None))
        return Review.objects.filter(watchlist__pk=self.kwargs.get('pk', None))
        # stream = get_object_or_404(
        #     StreamPlatform, watchlist=self.kwargs.get('pk', None))
        # return Review.objects.filter(watchlist__watchlist=stream)


class ReviewDetail(RetrieveUpdateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    lookup_url_kwarg = 'review_pk'
    permission_classes = [IsReviewUserOrReadOnly]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review-detail'
    # lookup = {'hull_no': hull_no} if pk is None else {'pk': pk}

    def get_serializer_context(self):
        context = super(ReviewDetail, self).get_serializer_context()
        context.update({"request": self.request})
        return context

    def get(self, request, review_pk, pk=None, *args, **kwargs):
        review = self.get_object()
        # print(review.pk)
        serializer = ReviewSerializer(
            review, context={'request': request})
        return Response(serializer.data)


# class ReviewDetail(RetrieveModelMixin, GenericAPIView, IsAuthenticated):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, re____quest, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)


# class ReviewList(ListModelMixin, CreateModelMixin, GenericAPIView, IsAuthenticated):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

class StreamPlatformR(ModelViewSet):
    queryset = StreamPlatform.objects.all()
    permission_classes = [IsAdminUser]

    # serializer_class = StreamPlatformSerializer

    def get_serializer_context(self):
        context = super(StreamPlatformR, self).get_serializer_context()
        context.update({"request": self.request})
        return context

    def create(self, request, *args, **kwargs):
        serializer = StreamPlatformSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# class StreamPlatformR(ViewSet):
#     def list(self, request):
#         queryset = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def retrieve(self, request, pk=None, *args, **kwargs):
#         queryset = StreamPlatform.objects.get(pk=pk)
#         serializer = StreamPlatformSerializer(queryset)
#         return Response(serializer.data)

#     def create(self, request, *args, **kwargs):
#         serializer = StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def destroy(self, request, *args, **kwargs):
#         return Response()


class StreamPlatformAV(APIView):
    permission_classes = [IsAdminUser, IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        stream = StreamPlatform.objects.all()
        serializers = StreamPlatformSerializer(
            stream, many=True, context={'request': request})
        print(request.user)
        return Response(serializers.data)

    def post(self, request, *args, **kwargs):
        serializers = StreamPlatformSerializer(
            data=request.data, context={'request': request})

        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class StreamPlatformDetailAV(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def get(self, request, *args, **kwargs):
        try:
            stream = StreamPlatform.objects.get(pk=self.kwargs.get("pk", None))
        except StreamPlatform.DoesNotExist:
            return Response({"error message": "StreamPlatform not found "}, status=status.HTTP_404_NOT_FOUND)
        serializers = StreamPlatformSerializer(
            stream, context={'request': request})
        return Response(serializers.data)

    def put(self, request, *args, **kwargs):
        stream = StreamPlatform.objects.get(pk=self.kwargs.get('pk', None))
        serializers = StreamPlatformSerializer(stream, data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        stream = StreamPlatform.objects.get(pk=self.kwargs.get('pk', None))
        stream.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class WatchListAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get(self, request, *args, **kwargs):
        movies = WatchList.objects.all()
        serializers = WatchListSerializer(movies, many=True)
        return Response(serializers.data)

    def post(self, request, *args, **kwargs):
        serializers = WatchListSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class WatchListDetailAV(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, *args, **kwargs):
        try:
            movie = WatchList.objects.get(pk=self.kwargs.get('pk', None))
        except WatchList.DoesNotExist:
            return Response({"error message": "Movie not found "}, status=status.HTTP_404_NOT_FOUND)

        serializers = WatchListSerializer(movie)
        return Response(serializers.data)

    def put(self, request, *args, **kwargs):
        try:
            movie = WatchList.objects.get(pk=self.kwargs.get('pk', None))
        except:
            return Response({"error message": "Movie not found "}, status=status.HTTP_404_NOT_FOUND)
        serializers = WatchListSerializer(movie, data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_200_OK)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        try:
            movie = WatchList.objects.get(pk=self.kwargs.get('pk', None))
        except:
            return Response({"error message": "Movie not found "}, status=status.HTTP_404_NOT_FOUND)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@ api_view(['GET', 'POST'])
def movie_list(request):
    if request.method == 'GET':
        movies = WatchList.objects.all()
        serializers = WatchListSerializer(movies, many=True)

        return Response(serializers.data)
    if request.method == "POST":
        serializers = WatchListSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors)


@ api_view(['GET', 'PATCH', 'DELETE'])
def movie(request, pk):
    print('got_enough_data')
    if request.method == 'GET':
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'Error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)

        serializers = WatchListSerializer(movie)
        return Response(serializers.data)
    if request.method == "PATCH":
        print('got_data')
        movie = WatchList.objects.get(pk=pk)
        serializers = WatchListSerializer(movie, data=request.data)
        if serializers.is_valid():
            serializers.save()
            print(serializers.data)

            return Response(serializers.data)
        else:
            return Response(serializers.errors)

    if request.method == "DELETE":
        print('got_data')
        movie = WatchList.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
