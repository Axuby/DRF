# from django.shortcuts import render
# from django.http import JsonResponse
# from .models import Movie

# # Create your views here.


# def movie_list(request):
#     movies = Movie.objects.all()

#     data = {
#         "movies": list(movies.values()),
#     }
#     for movies_obj in data["movies"]:
#         print(movies_obj["id"])
#     print(data)

#     return JsonResponse(data)
#     return render(request, "watchlist_app/movies.html", context)


# def movie(request, pk):
#     movie = Movie.objects.get(pk=pk)
#     data = {
#         "name": movie.name,
#         "description": movie.description,
#         'active': movie.is_active,
#     }

#     return JsonResponse(data)
