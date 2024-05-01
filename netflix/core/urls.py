from django.urls import path
from core import views

urlpatterns = [
    path("", views.index, name="home"),
    path("login/", views.login, name="login"),
    path("signup/", views.signup, name="signup"),
    path("logout/", views.logout, name="logout"),
    path("movie/<str:uuid>/", views.movie, name="movie"),
    path("serie/<str:uuid>/", views.serie, name="serie"),
    path("genre/<str:genre>/", views.genre, name="genre"),
    path("mylist/", views.mylist, name="mylist"),
    path("add-to-list/", views.add_to_list, name="add-to-list"),
    path("search/", views.search, name="search"),
    path("saison/", views.saison, name="saison"),
    path("saison-detail/<int:id>/", views.saison_detail, name="saison-detail"),
    path(
        "episode/<str:uuid>/<str:saison>/<str:episode>/", views.episode, name="episode"
    ),
]
