from django.db import models
from django.contrib.auth.models import User 




class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	bio = models.CharField(max_length=254, blank=True, null=True)
	picture = models.ImageField(upload_to='profile', default="img/default.png")


	def __str__(self):
		return self.user.username
