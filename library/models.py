# models.py
from django.db import models
from django.contrib.auth.models import User

class Genre(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название жанра")
    description = models.TextField(blank=True, verbose_name="Описание жанра")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

class Author(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя автора")
    bio = models.TextField(blank=True, verbose_name="Биография")
    avatar_url = models.URLField(blank=True, verbose_name="Ссылка на аватар")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    death_date = models.DateField(null=True, blank=True, verbose_name="Дата смерти")
    country = models.CharField(max_length=100, blank=True, verbose_name="Страна")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"

class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name="Автор") 
    genres = models.ManyToManyField(Genre, blank=True, verbose_name="Жанры")
    year = models.IntegerField(verbose_name="Год издания")
    pages = models.IntegerField(null=True, blank=True, verbose_name="Количество страниц")
    description = models.TextField(blank=True, verbose_name="Описание")
    cover_url = models.URLField(blank=True, verbose_name="Ссылка на обложку")
    file_url = models.URLField(blank=True, verbose_name="Ссылка на файл книги")
    is_featured = models.BooleanField(default=False, verbose_name="Рекомендуемая")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="Книга")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], verbose_name="Рейтинг")
    text = models.TextField(verbose_name="Текст отзыва")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        unique_together = ['book', 'user']

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="Книга")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранные"
        unique_together = ['user', 'book']