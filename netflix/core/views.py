import random
import re
from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib import auth
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from core import models


@login_required
def movie(request, uuid):
    movie = models.Movie.objects.get(uu_id=uuid)
    return render(request, "movie.html", context={"movie_details": movie})


@login_required
def genre(request, genre):
    movies = models.Movie.objects.filter(genre=genre)
    return render(request, "genre.html", context={"movies": movies, "genre": genre})


def add_to_list(request):
    if request.method == "POST":
        movie_url_id = request.POST.get("movie_id")
        uuid_regex = re.compile(
            r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-4[0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$"
        )
        if uuid_regex.match(movie_url_id):
            movie = get_object_or_404(models.Movie, uu_id=movie_url_id)
            movie_list, created = models.MovieList.objects.get_or_create(
                owner_user=request.user, movie=movie
            )
            if created:
                response_data = {"status": "created", "message": "Added to list"}
            else:
                response_data = {"status": "info", "message": "Movie already in list"}
            return JsonResponse(response_data)
        else:
            response_data = {"status": "error", "messages": "Invalid request"}
            return JsonResponse(response_data, status=400)
    else:
        pass


@login_required
def mylist(request):
    moviesList = models.MovieList.objects.filter(owner_user=request.user)
    movies = []
    for movieList in moviesList:
        movies.append(movieList.movie)

    return render(request, "my_list.html", context={"movies": movies})


@login_required
def search(request):
    if request.method == "POST":
        term = request.POST.get("search_term")
        movies = models.Movie.objects.filter(title__icontains=term)

        return render(request, "search.html", context={"movies": movies, "query": term})
    else:
        return render(request, "search.html")


@login_required
def index(request):
    movies = models.Movie.objects.all()
    featured_movie = None
    if len(movies) != 0:
        featured_movie = movies[random.randint(0, len(movies) - 1)]

    return render(
        request,
        "index.html",
        context={"movies": movies, "featured_movie": featured_movie},
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
