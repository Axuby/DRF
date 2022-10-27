from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

# Create your models here.


class StreamPlatform(models.Model):
    name = models.CharField(max_length=30)
    about = models.CharField(max_length=200, blank=True)
    website = models.URLField(max_length=100)

    def __str__(self) -> str:
        return self.name


class WatchList(models.Model):
    title = models.CharField(max_length=50)
    storyline = models.CharField(max_length=200)
    platform = models.ForeignKey(
        StreamPlatform, related_name="watchlist", on_delete=models.CASCADE, null=True, blank=True)
    number_of_ratings = models.IntegerField(default=0)
    avg_rating = models.FloatField(default=0)

    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    # def total(self):
    #     return self.review.count()


class Review(models.Model):
    review_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="review", null=True)
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    watchlist = models.ForeignKey(
        WatchList, related_name="reviews", on_delete=models.CASCADE, null=True)
    description = models.CharField(max_length=200, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.rating) + "|" + self.watchlist.title

# class Movie(models.Model):
#     name = models.CharField(max_length=50)
#     description = models.CharField(max_length=200)
#     is_active = models.BooleanField(default=False)

#     def __str__(self):
#         return self.name
