import random
import re
import json
from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib import auth
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from core import models


@login_required
def movie(request, uuid):
    movie = models.Movie.objects.get(uu_id=uuid)

    return render(request, "movie.html", context={"movie_details": movie})


@login_required
def episode(request, uuid, saison, episode):
    serie = models.Serie.objects.get(uu_id=uuid)
    episode = (
        models.Episode.objects.filter(serie=serie)
        .filter(saison=saison)
        .get(order=episode)
    )

    return render(request, "episode.html", context={"episode": episode})


def serie(request, uuid):
    serie = models.Serie.objects.get(uu_id=uuid)
    return render(request, "serie.html", context={"serie_details": serie})


@login_required
def genre(request, genre):
    movies = models.Movie.objects.filter(genre=genre)
    series = models.Serie.objects.filter(genre=genre)
    return render(
        request,
        "genre.html",
        context={"movies": movies, "series": series, "genre": genre},
    )


def add_to_list(request):
    created1 = False
    created2 = False
    if request.method == "GET":

        movie_url_id = request.GET.get("movie_id")
        type = request.GET.get("type")
        uuid_regex = re.compile(
            r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-4[0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$"
        )
        if uuid_regex.match(movie_url_id):

            if type == "serie":
                serie = models.Serie.objects.get(uu_id=movie_url_id)
                serie_list, created1 = models.MovieList.objects.get_or_create(
                    owner_user=request.user, serie=serie
                )
            else:
                movie = models.Movie.objects.get(uu_id=movie_url_id)
                movie_list, created2 = models.MovieList.objects.get_or_create(
                    owner_user=request.user, movie=movie
                )

            if created1 or created2:
                response_data = {"status": "created", "message": "Added to list"}
            else:
                response_data = {
                    "status": "info",
                    "message": "Already in list",
                }
            return JsonResponse(response_data)
        else:
            response_data = {"status": "error", "messages": "Invalid request"}
            return JsonResponse(response_data, status=400)


@login_required
def mylist(request):
    moviesList = models.MovieList.objects.filter(owner_user=request.user)
    movies = []
    series = []
    for movieList in moviesList:

        if movieList.movie is None:
            series.append(movieList.serie)
        else:
            movies.append(movieList.movie)

    return render(request, "my_list.html", context={"movies": movies, "series": series})


@login_required
def search(request):
    if request.method == "POST":
        term = request.POST.get("search_term")
        movies = models.Movie.objects.filter(title__icontains=term)
        series = models.Serie.objects.filter(title__icontains=term)

        return render(
            request,
            "search.html",
            context={"movies": movies, "series": series, "query": term},
        )
    else:
        return render(request, "search.html")


@login_required
def index(request):
    movies_and_series = []
    movies = models.Movie.objects.all()
    series = models.Serie.objects.all()
    movies_and_series.append(movies)
    movies_and_series.append(series)
    featured_movie_serie = movies_and_series[
        random.randint(0, len(movies_and_series) - 1)
    ]
    featured_movie_serie = featured_movie_serie[
        random.randint(0, len(featured_movie_serie) - 1)
    ]
    isMovie = featured_movie_serie.__class__ is models.Movie

    return render(
        request,
        "index.html",
        context={
            "movies": movies,
            "featured_movie": featured_movie_serie,
            "series": series,
            "isMovie": isMovie,
        },
    )


def signup(request):
    if request.method == "POST":
        email = request.POST["email"]
        username = request.POST["username"]
        password = request.POST["password"]
        password2 = request.POST["password2"]

        if password == password2:
            if get_user_model().objects.filter(email=email).exists():
                messages.info(request, "Email already in use")
                return redirect("signup")
            elif get_user_model().objects.filter(username=username).exists():
                messages.info(request, "Username already in use")
                return redirect("signup")
            else:
                user = get_user_model().objects.create_user(
                    email=email,
                    username=username,
                    password=password,
                )
                user.save()
                user_login = auth.authenticate(
                    request, username=username, password=password
                )
                if user_login is not None:
                    auth.login(request, user_login)
                    messages.success(
                        request,
                        f"Account created for {username}! You are now logged in.",
                    )
                    return redirect("home")
                else:
                    messages.warning(request, "Failed to create account")
                    return redirect("signup")
        else:
            messages.info(request, f"Passwords do not match.")
            return redirect("signup")

    else:

        return render(request, "signup.html")


def logout(request):
    auth.logout(request)
    return redirect("login")


def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user_login = auth.authenticate(request, username=username, password=password)
        if user_login is not None:
            auth.login(request, user_login)
            return redirect("home")
        else:
            messages.warning(request, "Invalid credentials")
            return redirect("login")
    else:
        return render(request, "login.html")


def saison(request):
    seasons_list = []
    seasons_dict = {}
    uuid = request.GET.get("uuid")
    seasons = models.Season.objects.filter(serie__uu_id=uuid)

    for season in seasons:
        season_dict = {"id": season.id, "name": season.name, "order": season.order}

        seasons_list.append(season_dict)
    seasons_dict["saisons"] = seasons_list[0]

    return HttpResponse(json.dumps(seasons_list))


def saison_detail(request, id):
    saison = models.Season.objects.get(pk=id)
    episodes = models.Episode.objects.filter(saison=saison).order_by("id")

    return render(
        request, "saison_detail.html", {"saison": saison, "episodes": episodes}
    )
