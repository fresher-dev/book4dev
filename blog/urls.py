from django.urls import path 
from . import views


app_name = "blog"


urlpatterns = [

	path("", views.home, name="home"),
	path("<slug:slug>", views.post_detail, name="detail"),
	path("<int:pk>/create/post", views.create_post, name="upload"),	
	path("posts/", views.blog_posts, name="posts"),
	path("delete/<slug:slug>/", views.delete_post, name="blog_delete"),
	path("<slug:slug>/edit/", views.edit_post, name="blog_edit"),
	path("check/<slug:slug>", views.check_yes_or_no, name="blog_check"),
]