from typing import Any
from django.contrib import admin
from django.db.models import Avg
from django.http.request import HttpRequest
from django.utils.html import format_html
from users.models import CustomUser
from stories.models import Story, Review, Rating


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'date_joined',
                    'is_superuser', 'is_active', 'is_staff']
    search_fields = ['username']


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'author', 'pub_date', 'average_rating'
    ]
    list_filter = ['title', 'author', 'pub_date']
    search_fields = ['title',]

    def get_queryset(self, request: HttpRequest):
        return super().get_queryset(request).\
            select_related('author')

    def average_rating(self, obj):
        return Rating.objects.\
            filter(story__id=obj.id).\
            aggregate(average_rating=Avg('rating'))['average_rating']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['author', 'story', 'pub_date']
    list_filter = ['author', 'story', 'pub_date']

    def get_queryset(self, request: HttpRequest):
        return super().get_queryset(request).\
            select_related('author').\
            select_related('story')
