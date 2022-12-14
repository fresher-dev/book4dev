from django import forms
from .models import Blog, BlogComment




class BlogForm(forms.ModelForm):
	class Meta:
		model = Blog
		fields = ["title", "body", "tags", "image", "status"]

	
	def __init__(self, *args, **kwargs):
		super(BlogForm, self).__init__(*args, *kwargs)

		for field in self.fields:
			self.fields[field].widget.attrs['class'] = "form-control"


		self.fields['image'].widget.attrs['accept'] = "image/*"


class BlogCommentForm(forms.ModelForm):
	class Meta:
		model = BlogComment
		fields = ["email", "body"]

	def __init__(self, *args, **kwargs):
		super(BlogCommentForm, self).__init__(*args, *kwargs)

		for field in self.fields:
			self.fields[field].widget.attrs['class'] = "form-control"



class BlogFormEdit(forms.ModelForm):
	class Meta:
		model = Blog
		fields = "__all__"
