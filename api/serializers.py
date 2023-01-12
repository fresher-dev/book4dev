from rest_framework import serializers
from book.models import Book
from blog.models import Blog


class BookSerializers(serializers.ModelSerializer):
	class Meta:
		model = Book
		fields = ["title", "author", "description", "file", "cover", "link", "tags"]


class BlogSerializers(serializers.ModelSerializer):
	class Meta:
		model = Blog
		fields = ["title", "body", "tags", "image", "status"]

