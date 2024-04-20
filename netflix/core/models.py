from django.db import models
from uuid import uuid4
from django.contrib.auth import get_user_model


# Create your models here.
class Movie(models.Model):
    GENRES_CHOICES = [
        ("action", "Action"),
        ("comedy", "Comedy"),
        ("crama", "Drama"),
        ("fantasy", "Fantasy"),
        ("romance", "Romance"),
        ("science_fiction", "Science Fiction"),
    ]
    uu_id = models.UUIDField(default=uuid4)
    title = models.CharField(max_length=255)
    description = models.TextField()
    release_date = models.DateField()
    genre = models.CharField(max_length=100, choices=GENRES_CHOICES)
    length = models.PositiveIntegerField()
    image_card = models.ImageField(upload_to="movies_images/")
    image_cover = models.ImageField(upload_to="movies_images/")
    video = models.FileField(upload_to="movies_video/")
    movie_views = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.title


class MovieList(models.Model):
    owner_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
