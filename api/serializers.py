from rest_framework import serializers
from book.models import Book
from blog.models import Blog


class BookSerializers(serializers.ModelSerializer):
    """
    Book Serializers Rest Framework
    Book Model
    """

    class Meta:
        model = Book
        fields = ["title", "author", "description", "file", "cover", "link", "tags"]


class BlogSerializers(serializers.ModelSerializer):
    """
    Blog Serializers Rest Framework
    Blog Model
    """

    class Meta:
        model = Blog
        fields = ["title", "body", "tags", "image", "status"]
