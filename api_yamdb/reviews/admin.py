from django.contrib import admin

from .models import User, Categories, Comment, Titles, Reviews, Genres, GenreTitle


admin.site.register(User)
admin.site.register(Categories)
admin.site.register(Comment)
admin.site.register(Titles)
admin.site.register(Reviews)
admin.site.register(Genres)
admin.site.register(GenreTitle)
