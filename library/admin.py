# admin.py
from django.contrib import admin
from .models import Author, Book

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    list_filter = ['created_at']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'year', 'created_at']
    search_fields = ['title', 'author__name']
    list_filter = ['year', 'author', 'created_at']
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'author', 'year', 'description')
        }),
        ('Обложка', {
            'fields': ('cover_url',),
            'description': 'Вставьте ссылку на изображение обложки'
        }),
    )