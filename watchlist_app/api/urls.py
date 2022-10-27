
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

# router.register('stream', views.StreamPlatformR,
#                 basename='streamplatform')
urlpatterns = [
    path('list/', views.WatchListAV.as_view(), name="movie-list"),
    path('<int:pk>/', views.WatchListDetailAV.as_view(), name="movie-detail"),
    path('stream/<int:pk>/', views.StreamPlatformDetailAV.as_view(),
         name="streamplatform-detail"),
    path('stream/', views.StreamPlatformAV.as_view(), name="stream-list"),
    # path('review/', views.ReviewList.as_view(), name="review-list"),
    # path('review/<int:review_pk>/',
    #      views.ReviewDetail.as_view(), name="review-detail"),
    #     path('', include(router.urls)),
    path('<int:pk>/review-create/',
         views.ReviewCreate.as_view(), name="review-create"),
    path('<int:pk>/reviews/',
         views.ReviewList.as_view(), name="review-list"),
    path('review/<int:review_pk>/',
         views.ReviewDetail.as_view(), name="review-detail"),
    path('review/<str:username>/',
         views.ReviewFromUser.as_view(), name="user-review-detail"),
    path('review/',
         views.SearchReviewFromUser.as_view(), name="search-user-review-detail"),
    path('movie/',
         views.SearchWatchList.as_view(), name="watch-review-detail"),
]
