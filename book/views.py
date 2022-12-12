from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, BookReview
from .forms import BookForm, BookReviewForm
from django.contrib.auth.models import User
from django.utils.text import slugify
from accounts.forms import ProfileForm
from django.urls import reverse
from accounts.models import Profile
from tags.models import Tag
from blog.models import Blog
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib.auth.decorators import login_required




def home(request):
	books = Book.objects.all()[:12]

	lastbook = Book.objects.all().order_by('-created_date')

	blogs = Blog.objects.all().order_by('-created_date')[:4]

	context = {
		"books": books,
		"lastbook": lastbook,
		"get_tags": Tag.objects.all(),
		"blogs": blogs,
	}

	return render(request, "book/home.html", context)


def book_explorer(request):
	lastbook = Book.objects.all().order_by("-created_date")

	paginator = Paginator(lastbook, 12)
	page = request.GET.get('page', 1)

	try:
		page_obj = paginator.page(page)

	except PageNotAnInteger:
		page_obj = paginator.page(1)

	except EmptyPage:
		page_obj = paginator.page(paginator.num_pages)

	context = {
		"lastbook": lastbook,
		"page_obj": page_obj,
		"page": page,
	}

	return render(request, "book/explorer.html", context)


def book_detail(request, slug):
	book = Book.objects.get(slug=slug)
	silder_book = Book.objects.all().order_by('-created_date')[:4]

	if request.method == "POST":
		form = BookReviewForm(request.POST, request.FILES)
		if form.is_valid():
			stars = form.cleaned_data['stars']
			body = form.cleaned_data['body']

			if request.user.is_authenticated:
				book_review = BookReview(user=request.user, stars=stars, body=body, book=book)
			else:
				book_review = BookReview(stars=stars, body=body, book=book)
			book_review.save()
			return redirect(reverse('book:book_detail', args=[book.slug]))
	else:
		form = BookReviewForm()

	context = {
		"book": book,
		"silder_book": silder_book,
		"form": form,
		"reviews": BookReview.objects.filter(book=book).order_by('created_date'),
	}

	return render(request, "book/detail.html", context)



def book_upload(request, pk):
	user = User.objects.get(id = pk)

	if request.method == "POST":
		form = BookForm(request.POST, request.FILES)

		if form.is_valid():
			title = form.cleaned_data['title']
			author = form.cleaned_data['author']
			description = form.cleaned_data['description']
			slug = slugify(title)
			file = form.cleaned_data['file']
			cover = form.cleaned_data['cover']
			link = form.cleaned_data['link']
			tags = form.cleaned_data['tags']

			book = Book.objects.create(title=title, author=author, user=user, description=description, 
										slug=slug, file=file, cover=cover, link=link)

			for tag in tags:
				book.tags.add(tag)
				book.save()
			return redirect("book:home")

	else:
		form = BookForm()

	context = {
		"form": form
	}

	return render(request, "book/book_upload.html", context)



def book_user_profile(request, pk):
	book_user = User.objects.get(id = pk)

	books = Book.objects.filter(user=book_user)[::-1]
	posts = Blog.objects.filter(user=book_user)[::-1]
	context = {
		"bookuser": book_user,
		"books": books,
		"posts": posts,
	}

	return render(request, "book/book_user_profile.html", context)


def book_user_create_profile(request, pk):
	user = User.objects.get(id = pk)

	# profile, create = Profile.objects.get_or_create(user=user)

	try:
		profile = request.user.profile
	except Profile.DoesNotExist:
		profile = Profile(user=request.user)


	if request.method == "POST":
		form = ProfileForm(request.POST, request.FILES, instance=profile)

		if form.is_valid():
			bio = form.cleaned_data['bio']
			picture = form.cleaned_data['picture']
		
			newform = form.save(commit=False)
			newform.bio = bio 
			newform.picture = picture

			newform.save()

			return redirect(reverse("book:book_user_profile", args=[request.user.id]))
	else:
		form = ProfileForm(instance=profile)

	context = {
		"form": form,
	}

	return render(request, "accounts/create_book_profile.html", context)




def view_tags(request, name):
	tag = Tag.objects.get(name=name)
	books = tag.book_set.all()
	posts = tag.blog_set.all()

	context = {
		"tag": tag,
		"books": books,
		"posts": posts,
		"get_tags": Tag.objects.all(),
		"lastbook": Book.objects.all().order_by('-created_date')[:2],
	}

	return render(request, "book/categories.html", context)



def search(request):
	if request.method == "GET":
		queryset = request.GET.get("q")

		if queryset is not None:
			book_results = Book.objects.filter(Q(title__icontains=queryset))
			blog_results = Blog.objects.filter(Q(title__icontains=queryset))

	context = {
		"book_results": book_results,
		"blog_results": blog_results,
		"lastbook": Book.objects.all().order_by('-created_date')[:2],
		"get_tags": Tag.objects.all(),
	}

	return render(request, "book/search.html", context)

@login_required
def check_yes_or_no(request, slug):

	book = get_object_or_404(Book, slug=slug)

	context = {
		"book": book,
	}

	return render(request, "book/check_yes_or_no.html", context)


@login_required
def delete_book(request, slug):

	book = get_object_or_404(Book, slug=slug)

	book.delete()

	return redirect(reverse("book:book_user_profile", args=[request.user.id]))

@login_required
def edit_book(request, slug):
	book = get_object_or_404(Book, slug=slug)

	if request.method == "POST":
		form = BookForm(request.POST, request.FILES, instance=book)

		if form.is_valid():
			newform = form.save(commit=False)
			newform.user = request.user
			newform.save()
			return redirect(reverse("book:book_user_profile", args=[book.user.id]))

	else:
		form = BookForm(instance=book)

	context = {
		"form": form,
	}

	return render(request, "book/book_upload.html", context)
