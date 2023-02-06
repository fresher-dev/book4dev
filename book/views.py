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
from django.core.mail import send_mail
from django.conf import settings


def home(request):
    """
    Book Home
    -> show all book order by create date
    """
    books = Book.objects.all()[:12]

    lastbook = Book.objects.all().order_by("-created_date")

    blogs = Blog.objects.all().order_by("-created_date")[:4]

    context = {
        "books": books,
        "lastbook": lastbook,
        "get_tags": Tag.objects.all(),
        "blogs": blogs,
    }

    return render(request, "book/home.html", context)


def book_explorer(request):
    """
    Book Page Paginator
    """
    lastbook = Book.objects.all().order_by("-created_date")

    paginator = Paginator(lastbook, 12)
    page = request.GET.get("page", 1)

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
    """
    Book Detail
    -> detail book
    -> review book
    -> download book or link book
    """
    book = Book.objects.get(slug=slug)
    silder_book = Book.objects.all().order_by("-created_date")[:4]

    if request.method == "POST":
        form = BookReviewForm(request.POST, request.FILES)
        if form.is_valid():
            stars = form.cleaned_data["stars"]
            body = form.cleaned_data["body"]

            if request.user.is_authenticated:
                book_review = BookReview(
                    user=request.user, stars=stars, body=body, book=book
                )
            else:
                book_review = BookReview(stars=stars, body=body, book=book)
            book_review.save()
            return redirect(reverse("book:book_detail", args=[book.slug]))
    else:
        form = BookReviewForm()

    context = {
        "book": book,
        "silder_book": silder_book,
        "form": form,
        "reviews": BookReview.objects.filter(book=book).order_by("created_date"),
    }

    return render(request, "book/detail.html", context)


def book_upload(request, pk):
    """
    Book Upload
    -> create new book
    -> new book save with BookForm class
    """
    user = User.objects.get(id=pk)

    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)

        if form.is_valid():
            title = form.cleaned_data["title"]
            author = form.cleaned_data["author"]
            description = form.cleaned_data["description"]
            slug = slugify(title)
            file = form.cleaned_data["file"]
            cover = form.cleaned_data["cover"]
            link = form.cleaned_data["link"]
            tags = form.cleaned_data["tags"]

            book = Book.objects.create(
                title=title,
                author=author,
                user=user,
                description=description,
                slug=slug,
                file=file,
                cover=cover,
                link=link,
            )

            for tag in tags:
                book.tags.add(tag)
                book.save()
            return redirect("book:home")

    else:
        form = BookForm()

    context = {"form": form}

    return render(request, "book/book_upload.html", context)


def book_user_profile(request, pk):
    """
    User Account Profile
    -> show who upload book with user profile
    """
    book_user = User.objects.get(id=pk)

    books = Book.objects.filter(user=book_user)[::-1]
    posts = Blog.objects.filter(user=book_user)[::-1]
    context = {
        "bookuser": book_user,
        "books": books,
        "posts": posts,
    }

    return render(request, "book/book_user_profile.html", context)


def book_user_create_profile(request, pk):
    """
    User profile create
    -> if user account is create profile:
            -> show user profile
    -> else:
            -> create new profile with user
            -> show user profile
    """
    user = User.objects.get(id=pk)

    # profile, create = Profile.objects.get_or_create(user=user)

    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            bio = form.cleaned_data["bio"]
            picture = form.cleaned_data["picture"]

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
	"""
	Book and Blog tags
	-> show all book tags
	-> show all blog tags
	"""
    tag = Tag.objects.get(name=name)
    books = tag.book_set.all()
    posts = tag.blog_set.all()

    context = {
        "tag": tag,
        "books": books,
        "posts": posts,
        "get_tags": Tag.objects.all(),
        "lastbook": Book.objects.all().order_by("-created_date")[:2],
    }

    return render(request, "book/categories.html", context)


def search(request):
	"""
	Search Function
	-> search all blog and book with title
	"""
    if request.method == "GET":
        queryset = request.GET.get("q")

        if queryset is not None:
            book_results = Book.objects.filter(Q(title__icontains=queryset))
            blog_results = Blog.objects.filter(Q(title__icontains=queryset))

    context = {
        "book_results": book_results,
        "blog_results": blog_results,
        "lastbook": Book.objects.all().order_by("-created_date")[:2],
        "get_tags": Tag.objects.all(),
    }

    return render(request, "book/search.html", context)


@login_required
def check_yes_or_no(request, slug):
	"""
	Book user checking page
	"""
    book = get_object_or_404(Book, slug=slug)

    context = {
        "book": book,
    }

    return render(request, "book/check_yes_or_no.html", context)


@login_required
def delete_book(request, slug):
	"""
	Delete book
	-> delet book
	"""
    book = get_object_or_404(Book, slug=slug)

    book.delete()

    return redirect(reverse("book:book_user_profile", args=[request.user.id]))


@login_required
def edit_book(request, slug):
	"""
	Update book
	-> book update with BookFrom class
	"""
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


def content_mail(request):
	"""
	User conent email
	-> send mail to user by django admin account
	"""

    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        messages = request.POST["messages"]

        subject = "Welcome to Book4Dev Django Web Mail Services"
        message = f"\nYour messages\n--------------------------\n{messages}\n--------------------------\n\nHi {username}, thank you for your attention."
        email_form = settings.EMAIL_HOST_USER
        receipient_list = [email]
        send_mail(subject, message, email_form, receipient_list)
        return redirect("book:home")
    return render(request, "book/content_form.html")
