from django.contrib import admin
from core import models

# Register your models here.


admin.site.register(models.Movie)
admin.site.register(models.MovieList)
admin.site.register(models.Episode)
admin.site.register(models.Season)
admin.site.register(models.Serie)
