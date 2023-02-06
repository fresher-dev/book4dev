from django.contrib import admin
from .models import Book, BookReview


class BookAdmin(admin.ModelAdmin):
    """
    BookAdmin model Admin
    -> auto create slug with title
    """

    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Book, BookAdmin)
admin.site.register(BookReview)
