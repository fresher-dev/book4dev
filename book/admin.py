from django.contrib import admin
from .models import Book, BookReview



class BookAdmin(admin.ModelAdmin):
	prepopulated_fields = {
		"slug": ("title", )
	}




admin.site.register(Book, BookAdmin)
admin.site.register(BookReview)
