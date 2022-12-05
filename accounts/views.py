from django.shortcuts import render, redirect
from .models import Profile
from django.contrib.auth.models import User 
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate


def sing_up(request):

	if request.method == "POST":
		username = request.POST.get("username")
		email = request.POST.get("email")
		password1 = request.POST.get("password-1")
		password2 = request.POST.get("password-2")

		if password1 == password2:
			if User.objects.filter(username=username).exists():
				messages.info(request, "Username is already exists!")
				return redirect("accounts:login")
			if User.objects.filter(email=email).exists():
				messages.info(request, "Email is already exists!")
				return redirect("accounts:login")
			else:
				user = User.objects.create_user(username=username, email=email, password=password1)
				user.save()
				# successful and instance create profile
				profile = Profile.objects.create(user=user)
				profile.save()
				messages.success(request, "Register is successfully!")
				return redirect("accounts:login")

		else:
			messages.error(request, "Wrong password!")
			return redirect("accounts:register")



	return render(request, "accounts/register.html")


def sing_in(request):
	if request.method == "POST":
		username = request.POST.get("username")
		password1 = request.POST.get('password-1')

		user = authenticate(username=username, password=password1)

		if user is not None:
			login(request, user)
			messages.success(request, "Login successfully")
			return redirect("book:home")
		else:
			messages.error(request, "Wrong Username and Password")
			return redirect("accounts:login")

	return render(request, "accounts/login.html")



def sing_out(request):
	logout(request)
	return redirect("book:home")