from django.shortcuts import render
from .serializers import BookSerializers, BlogSerializers
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions
from book.models import Book
from blog.models import Blog


class BookListApiView(ListCreateAPIView):
	# add permission to check if user if authenticated
	permission_classes = [permissions.IsAuthenticated]
	serializer_class = BookSerializers
	queryset = Book.objects.all()

class BookUpdateApiView(RetrieveUpdateDestroyAPIView):
	# add permission to check if user if authenticated
	permission_classes = [permissions.IsAuthenticated]
	serializer_class = BookSerializers
	queryset = Book.objects.all()


class BlogListApiView(ListCreateAPIView):
	# add permission to check if user if authenticated
	permission_classes = [permissions.IsAuthenticated]
	serializer_class = BlogSerializers
	queryset = Blog.objects.all()

class BlogUpdateApiView(RetrieveUpdateDestroyAPIView):
	# add permission to check if user if authenticated
	permission_classes = [permissions.IsAuthenticated]
	serializer_class = BlogSerializers
	queryset = Blog.objects.all()


def home(request):
	return render(request, "api/home.html")