from django.conf import settings
from django.conf.urls.static import static
from django.urls import path 
from . import views



app_name = "book"


urlpatterns = [
	path("", views.home, name="home"),
	path("explorer", views.book_explorer, name="explorer"),
	path("<slug:slug>", views.book_detail, name="book_detail"),
	path("<int:pk>/upload", views.book_upload, name="book_upload"),
	path("user/<int:pk>", views.book_user_profile, name="book_user_profile"),
	path("tag/<str:name>", views.view_tags, name="view_tags"),
	path("create/<int:pk>/profile", views.book_user_create_profile, name="create_profile"),
	path("search/", views.search, name="search"),

]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)