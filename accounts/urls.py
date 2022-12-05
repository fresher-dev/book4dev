from django.urls import path 
from . import views 


app_name = "accounts"


urlpatterns = [

	path("register", views.sing_up, name="register"),
	path("login", views.sing_in, name="login"),
	path("logout", views.sing_out, name="logout"),

]