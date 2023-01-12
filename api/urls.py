from django.urls import path 
from . import views


app_name = "api"

urlpatterns = [
	path("home/", views.home, name="home"),
	path("booklist/", views.BookListApiView.as_view(), name="booklist"),
	path("bookupdate/<int:pk>/", views.BookUpdateApiView.as_view(), name="bookupdate"),
	path("bloglist/", views.BlogListApiView.as_view(), name="bloglist"),
	path("blogupdate/<int:pk>/", views.BlogUpdateApiView.as_view(), name="blogupdate"),
]
