# admin.py
from django.contrib import admin
from .models import Genre, Author, Book, Review, Favorite

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'book_count']
    search_fields = ['name']
    list_filter = ['name']
    
    def book_count(self, obj):
        return obj.book_set.count()
    book_count.short_description = 'Количество книг'

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'birth_date', 'book_count', 'created_at']
    search_fields = ['name', 'country']
    list_filter = ['country', 'created_at']
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'bio', 'country', 'birth_date', 'death_date')
        }),
        ('Аватар', {
            'fields': ('avatar_url',),
            'description': 'Вставьте ссылку на изображение аватара автора'
        }),
    )
    
    def book_count(self, obj):
        return obj.book_set.count()
    book_count.short_description = 'Количество книг'

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'year', 'pages', 'is_featured', 'created_at']
    search_fields = ['title', 'author__name', 'description']
    list_filter = ['year', 'author', 'genres', 'is_featured', 'created_at']
    filter_horizontal = ['genres']
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'author', 'genres', 'year', 'pages', 'description')
        }),
        ('Медиа', {
            'fields': ('cover_url', 'file_url'),
            'description': 'Ссылки на обложку и файл книги'
        }),
        ('Дополнительно', {
            'fields': ('is_featured',),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author').prefetch_related('genres')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['book', 'user', 'rating', 'created_at']
    search_fields = ['book__title', 'user__username', 'text']
    list_filter = ['rating', 'created_at']
    readonly_fields = ['created_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('book', 'user')

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'created_at']
    search_fields = ['user__username', 'book__title']
    list_filter = ['created_at']
    readonly_fields = ['created_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'book')

# Настройка админ-панели
admin.site.site_header = 'Панель управления библиотекой'
admin.site.site_title = 'Библиотека'
admin.site.index_title = 'Управление контентом'