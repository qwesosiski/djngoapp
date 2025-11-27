# views.py
from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect
from .models import Book, Author, Genre, Review, Favorite

def home(request):
    # Фильтруем только книги с авторами
    featured_books = Book.objects.filter(is_featured=True, author__isnull=False).prefetch_related('genres', 'author')[:6]
    recent_books = Book.objects.filter(author__isnull=False).prefetch_related('genres', 'author').order_by('-created_at')[:8]
    total_books = Book.objects.filter(author__isnull=False).count()
    total_authors = Author.objects.count()
    total_genres = Genre.objects.count()
    
    # Получаем популярные жанры (с наибольшим количеством книг)
    popular_genres = Genre.objects.annotate(book_count=Count('book')).order_by('-book_count')[:6]
    
    return render(request, 'home.html', {
        'featured_books': featured_books,
        'recent_books': recent_books,
        'total_books': total_books,
        'total_authors': total_authors,
        'total_genres': total_genres,
        'popular_genres': popular_genres
    })

def book_list(request):
    # Фильтруем только книги с авторами
    books = Book.objects.filter(author__isnull=False).prefetch_related('genres', 'author')
    
    search_query = request.GET.get('search', '')
    year_filter = request.GET.get('year', '')
    sort_order = request.GET.get('sort', '-year')
    
    # Поиск по названию, автору и описанию
    if search_query:
        books = books.filter(
            Q(title__icontains=search_query) |
            Q(author__name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Фильтр по году
    if year_filter:
        books = books.filter(year=year_filter)
    
    # Сортировка по году
    if sort_order == 'year':
        books = books.order_by('year')
    else:
        books = books.order_by('-year')
    
    # Получаем список всех годов для выпадающего списка (только книги с авторами)
    all_years = Book.objects.filter(author__isnull=False).values_list('year', flat=True).distinct().order_by('-year')
    
    return render(request, 'books.html', {
        'books': books,
        'search_query': search_query,
        'year_filter': year_filter,
        'sort_order': sort_order,
        'all_years': all_years
    })

def book_detail(request, book_id):
    # Используем select_related для автора и prefetch_related для жанров
    book = get_object_or_404(
        Book.objects.select_related('author').prefetch_related('genres'), 
        id=book_id
    )
    reviews = Review.objects.filter(book=book).select_related('user').order_by('-created_at')
    
    return render(request, 'book_detail.html', {
        'book': book,
        'reviews': reviews
    })

def author_detail(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    # Фильтруем только книги с авторами (хотя здесь всегда будут книги этого автора)
    books = Book.objects.filter(author=author).prefetch_related('genres')
    
    return render(request, 'author_detail.html', {
        'author': author,
        'books': books
    })

def author_list(request):
    # Аннотируем количество книг (только книги с авторами)
    authors = Author.objects.annotate(
        book_count=Count('book', filter=Q(book__author__isnull=False))
    ).order_by('-book_count', 'name')
    return render(request, 'author_list.html', {'authors': authors})

def genre_list(request):
    # Аннотируем количество книг в каждом жанре (только книги с авторами)
    genres = Genre.objects.annotate(
        book_count=Count('book', filter=Q(book__author__isnull=False))
    ).order_by('-book_count')
    return render(request, 'genre_list.html', {'genres': genres})

def genre_detail(request, genre_id):
    genre = get_object_or_404(Genre, id=genre_id)
    # Фильтруем только книги с авторами
    books = Book.objects.filter(genres=genre, author__isnull=False).prefetch_related('genres', 'author')
    return render(request, 'genre_detail.html', {
        'genre': genre,
        'books': books
    })

@login_required
def add_review(request, book_id):
    if request.method == 'POST':
        book = get_object_or_404(Book, id=book_id)
        rating = request.POST.get('rating')
        text = request.POST.get('text')
        
        if not rating or not text:
            # Можно добавить сообщение об ошибке
            return redirect('book_detail', book_id=book_id)
        
        # Проверяем, не оставлял ли пользователь уже отзыв
        existing_review = Review.objects.filter(book=book, user=request.user).first()
        if existing_review:
            # Обновляем существующий отзыв
            existing_review.rating = rating
            existing_review.text = text
            existing_review.save()
        else:
            # Создаем новый отзыв
            Review.objects.create(book=book, user=request.user, rating=rating, text=text)
        
        return redirect('book_detail', book_id=book_id)
    
    # Если не POST запрос, перенаправляем на страницу книги
    return redirect('book_detail', book_id=book_id)

@login_required
def toggle_favorite(request, book_id):
    if request.method == 'POST':
        book = get_object_or_404(Book, id=book_id)
        favorite, created = Favorite.objects.get_or_create(user=request.user, book=book)
        
        if not created:
            favorite.delete()
            is_favorite = False
        else:
            is_favorite = True
            
        return JsonResponse({'is_favorite': is_favorite})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)