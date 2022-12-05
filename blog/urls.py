from django.urls import path 
from . import views


app_name = "blog"


urlpatterns = [

	path("", views.home, name="home"),
	path("<slug:slug>", views.post_detail, name="detail"),
	path("<int:pk>/create/post", views.create_post, name="upload"),	
	path("posts/", views.blog_posts, name="posts"),
]