# views.py
from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count
from .models import Book, Author

def book_list(request):
    books = Book.objects.all()
    
    search_query = request.GET.get('search', '')
    year_filter = request.GET.get('year', '')
    sort_order = request.GET.get('sort', '-year')  # По умолчанию новые сначала
    
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
        books = books.order_by('year')  # Старые сначала
    else:
        books = books.order_by('-year')  # Новые сначала
    
    # Получаем список всех годов для выпадающего списка
    all_years = Book.objects.values_list('year', flat=True).distinct().order_by('-year')
    
    return render(request, 'books.html', {
        'books': books,
        'search_query': search_query,
        'year_filter': year_filter,
        'sort_order': sort_order,
        'all_years': all_years
    })

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'book_detail.html', {'book': book})

def author_detail(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    books = Book.objects.filter(author=author)
    return render(request, 'author_detail.html', {
        'author': author,
        'books': books
    })

def author_list(request):
    authors = Author.objects.annotate(book_count=Count('book')).order_by('-book_count', 'name')
    return render(request, 'author_list.html', {'authors': authors})