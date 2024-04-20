from django.urls import path
from core import views

urlpatterns = [
    path("", views.index, name="home"),
    path("login/", views.login, name="login"),
    path("signup/", views.signup, name="signup"),
    path("logout/", views.logout, name="logout"),
    path("movie/<str:uuid>/", views.movie, name="movie"),
    path("genre/<str:genre>/", views.genre, name="movie"),
    path("mylist/", views.mylist, name="mylist"),
    path("add-to-list/", views.add_to_list, name="add-to-list"),
    path("search/", views.search, name="search"),
]
