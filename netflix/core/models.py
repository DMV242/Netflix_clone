from django.db import models
from uuid import uuid4
from django.contrib.auth import get_user_model


# Create your models here.
class Oeuvre(models.Model):
    GENRES_CHOICES = [
        ("action", "Action"),
        ("comedy", "Comedy"),
        ("drama", "Drama"),
        ("fantasy", "Fantasy"),
        ("romance", "Romance"),
        ("science_fiction", "Science Fiction"),
    ]
    uu_id = models.UUIDField(default=uuid4, editable=False, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    release_date = models.DateField()
    genre = models.CharField(max_length=100, choices=GENRES_CHOICES)
    length = models.PositiveIntegerField()
    image_card = models.ImageField(upload_to="movies_images/")
    image_cover = models.ImageField(upload_to="movies_images/")

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.title


class Movie(Oeuvre):
    video = models.FileField(upload_to="movies_video/")
    movie_views = models.IntegerField(default=0)


class Serie(Oeuvre):
    pass


class Season(models.Model):
    name = models.CharField(max_length=255)
    order = models.PositiveIntegerField()
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Saison {self.order} : " + self.serie.title + " - " + self.name


class Episode(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    order = models.PositiveIntegerField()
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE)
    saison = models.ForeignKey(Season, on_delete=models.CASCADE)
    video = models.FileField(upload_to="serie_video/")

    def __str__(self) -> str:
        return self.serie.title + " - " + self.title


class MovieList(models.Model):
    owner_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True, blank=True)
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE, null=True, blank=True)
