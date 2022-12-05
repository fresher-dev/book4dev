from django import forms
from .models import Book, BookReview




class BookForm(forms.ModelForm):
	class Meta:
		model = Book
		fields = ["title", "author", "description", "file", "cover", "link", "tags"]


	def __init__(self, *args, **kwargs):
		super(BookForm, self).__init__(*args, **kwargs)

		for field in self.fields:
			self.fields[field].widget.attrs['class'] = "form-control"
			if self.fields['tags']:
				continue
			if self.fields['created_date']:
				continue


		self.fields['tags'].widget.attrs['class'] = 'form-select'
		self.fields['file'].widget.attrs['accept'] = ".pdf"
		self.fields['cover'].widget.attrs['accept'] = "image/*"



class BookReviewForm(forms.ModelForm):
	class Meta:
		model = BookReview
		fields = ['stars', 'body']

	def __init__(self, *args, **kwargs):
		super(BookReviewForm, self).__init__(*args, **kwargs)

		for field in self.fields:
			self.fields[field].widget.attrs['class'] = 'form-control'
