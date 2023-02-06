from django.shortcuts import render
from .serializers import BookSerializers, BlogSerializers
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions
from book.models import Book
from blog.models import Blog


class BookListApiView(ListCreateAPIView):
    """
    Book List API View
    show all books api
    add permission to check if user if authenticated
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BookSerializers
    queryset = Book.objects.all()


class BookUpdateApiView(RetrieveUpdateDestroyAPIView):
    """
    Book Update and Delete API View
    add permission to check if user if authenticated
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BookSerializers
    queryset = Book.objects.all()


class BlogListApiView(ListCreateAPIView):
    """
    Blog List API View
    add permission to check if user if authenticated
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BlogSerializers
    queryset = Blog.objects.all()


class BlogUpdateApiView(RetrieveUpdateDestroyAPIView):
    """
    Blog Update and Delete API View
    add permission to check if user if authenticated
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BlogSerializers
    queryset = Blog.objects.all()


def home(request):
    """
    API Home Page
    API all list here
    """
    return render(request, "api/home.html")
