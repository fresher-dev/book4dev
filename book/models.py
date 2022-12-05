from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from tags.models import Tag



class Book(models.Model):
	title = models.CharField(max_length=200)
	author = models.CharField(max_length=100, null=True, blank=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	description = models.TextField(null=True, blank=True)
	slug = models.SlugField()
	file = models.FileField(upload_to="books", null=True, blank=True)
	cover = models.ImageField(upload_to="images", default="img/book.jpg")
	link = models.CharField(max_length=2084, null=True, blank=True)
	tags = models.ManyToManyField(Tag, blank=True)
	created_date = models.DateTimeField(default=timezone.now)
	edited_date = models.DateTimeField(auto_now_add=True)


	def __str__(self):
		return self.title
	


class BookReview(models.Model):
	CHOICE_STARS = (
		(1, 1), 
		(2, 2),
		(3, 3),
		(4, 4),
		(5, 5)
	)

	user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
	stars = models.IntegerField(choices=CHOICE_STARS, default=5)
	body = models.TextField(blank=True, null=True)
	book = models.ForeignKey(Book, on_delete=models.CASCADE)
	created_date = models.DateTimeField(default=timezone.now)


	def __str__(self):

		if self.user is None:
			user = "AnonymousUser"
		else:
			user = self.user	
		return "{} books ({}) stars by {}.".format(self.book.title, self.stars, user)
