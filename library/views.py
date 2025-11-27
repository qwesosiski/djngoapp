# views.py
from django.shortcuts import render
from django.db.models import Q
from .models import Book

def book_list(request):
    books = Book.objects.all()
    
    search_query = request.GET.get('search', '')
    if search_query:
        books = books.filter(
            Q(title__icontains=search_query) |
            Q(author__name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    return render(request, 'books.html', {
        'books': books,
        'search_query': search_query
    })