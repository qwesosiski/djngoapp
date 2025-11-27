# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('books/', views.book_list, name='book_list'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('author/<int:author_id>/', views.author_detail, name='author_detail'),
    path('authors/', views.author_list, name='author_list'),
    path('genres/', views.genre_list, name='genre_list'),
    path('genre/<int:genre_id>/', views.genre_detail, name='genre_detail'),
    path('book/<int:book_id>/review/', views.add_review, name='add_review'),
    path('book/<int:book_id>/favorite/', views.toggle_favorite, name='toggle_favorite'),
]