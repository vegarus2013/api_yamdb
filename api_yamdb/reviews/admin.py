from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title, User


class TitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'year', 'description', 'category')
    search_fields = ('name',)
    list_filter = ('genre', 'category')
    empty_value_display = '-пусто-'


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'author', 'score', 'title', 'pub_date')
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'author', 'review', 'pub_date')
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


admin.site.register(User)
admin.site.register(Category)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Genre)
