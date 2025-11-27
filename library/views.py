# views.py
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Book, Author

def book_list(request):
    books = Book.objects.all()
    search_query = request.GET.get('search', '')
    if search_query:
        books = books.filter(
            Q(title__icontains=search_query) |
            Q(author__name__icontains=search_query)
        )
    return render(request, 'books.html', {'books': books, 'search_query': search_query})

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