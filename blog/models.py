from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from tags.models import Tag
from ckeditor_uploader.fields import RichTextUploadingField



class Blog(models.Model):

	STATUS_CHOICE = (
		(0, "Draft"),
		(1, "Public"),
	)

	title = models.CharField(max_length=254)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	slug = models.SlugField()
	body = RichTextUploadingField(blank=True)
	created_date = models.DateTimeField(default=timezone.now)
	edited_date = models.DateTimeField(auto_now_add=True)
	tags = models.ManyToManyField(Tag, blank=True)
	image = models.ImageField(upload_to=None, null=True, blank=True)
	status = models.IntegerField(choices=STATUS_CHOICE, default=0)


	def __str__(self):
		return self.title


class BlogComment(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
	email = models.EmailField(blank=True, null=True, unique=True)
	body = models.TextField(null=True, blank=True)
	blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
	created_date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		if self.user is None:
			user = "AnonymousUser"
		else:
			user = self.user	

		return "{} comment by {}.".format(self.blog.title, user)

