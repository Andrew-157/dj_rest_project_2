from django.contrib import admin
from fiction.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'slug'
    ]
    list_filter = ['title', 'slug']
    search_fields = ['title', 'slug']
