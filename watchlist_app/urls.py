
from django.urls import path, include
from . import views

urlpatterns = [
    path('list/', views.movie_list),
    path('<int:pk>/', views.movie),
]
