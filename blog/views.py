from django.shortcuts import render, redirect, get_object_or_404
from .models import Blog, BlogComment
from tags.models import Tag
from .forms import BlogForm, BlogCommentForm, BlogFormEdit
from django.utils.text import slugify
from django.contrib.auth.models import User
from random import shuffle
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from django.contrib.auth.decorators import login_required


def home(request):
    """
    Blog Home Page
    -> Show all blog post -> random
    -> Last Posts
    -> Tags all tags
    """
    post_all = Blog.objects.filter(status=1).order_by("-created_date")[:6]

    lasts_post = Blog.objects.order_by("-created_date")[:1:0].get()

    posts = []

    for post in post_all:
        posts.append(post)

    shuffle(posts)

    context = {
        "posts": posts,
        "get_tags": Tag.objects.all(),
        "lastposts": Blog.objects.all().order_by("-created_date")[:3],
        "lasts": lasts_post,
    }

    return render(request, "blog/blog_home.html", context)


def post_detail(request, slug):
    """
    Blog Post Detail
    -> post detail page
    -> comment function
    """
    post = Blog.objects.get(slug=slug)

    if request.method == "POST":
        form = BlogCommentForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            body = form.cleaned_data["body"]

            if request.user.is_authenticated:
                user = request.user
                blog_comment = BlogComment(user=user, email=email, body=body, blog=post)
            else:
                blog_comment = BlogComment(email=email, body=body, blog=post)

            blog_comment.save()

            return redirect(reverse("blog:detail", args=[post.slug]))
    else:
        form = BlogCommentForm()

    context = {
        "post": post,
        "get_tags": Tag.objects.all(),
        "lastposts": Blog.objects.all().order_by("-created_date")[:3],
        "form": form,
        "comments": BlogComment.objects.filter(blog=post).order_by("created_date"),
    }

    return render(request, "blog/blog_detail.html", context)


def create_post(request, pk):
    """
    Create new blog post
    -> create new blog post in BlogForm class
    """
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)

        if form.is_valid():
            title = form.cleaned_data["title"]
            user = User.objects.get(id=pk)
            slug = slugify(title)
            body = form.cleaned_data["body"]
            tags = form.cleaned_data["tags"]
            image = form.cleaned_data["image"]
            status = form.cleaned_data["status"]

            post = Blog.objects.create(
                title=title, user=user, slug=slug, body=body, image=image, status=status
            )

            for item in tags:
                post.tags.add(item)
                post.save()

            return redirect("blog:home")
    else:
        form = BlogForm()

    context = {
        "form": form,
    }

    return render(request, "blog/blog_upload.html", context)


def blog_posts(request):
    """
    Show all blog post paginator page
    """
    recent_posts = Blog.objects.all().order_by("-created_date")[:5]
    all_tags = Tag.objects.all()
    blogs = Blog.objects.all().order_by("created_date")

    page = request.GET.get("page", 1)
    paginator = Paginator(blogs, 5)

    try:
        page_obj = paginator.page(page)

    except PageNotAnInteger:
        page_obj = paginator.page(1)

    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {
        "recent_posts": recent_posts,
        "all_tags": all_tags,
        "blogs": blogs,
        "page_obj": page_obj,
        "page": page,
    }

    return render(request, "blog/blog_posts.html", context)


@login_required
def delete_post(request, slug):
    """
    Blog Delete Post
    """
    post = get_object_or_404(Blog, slug=slug)

    post.delete()

    return redirect(reverse("book:book_user_profile", args=[request.user.id]))


@login_required
def edit_post(request, slug):
    """
    Blog Update Post
    -> update with BlogFromEdit class
    """
    post = get_object_or_404(Blog, slug=slug)

    if request.method == "POST":
        form = BlogFormEdit(request.POST, request.FILES, instance=post)

        if form.is_valid():
            newform = form.save(commit=False)
            newform.user = request.user
            newform.save()
            return redirect(reverse("book:book_user_profile", args=[post.user.id]))

    else:
        form = BlogFormEdit(instance=post)

    context = {
        "form": form,
    }

    return render(request, "book/book_upload.html", context)


@login_required
def check_yes_or_no(request, slug):
    """
    Blog user checking page
    """
    post = get_object_or_404(Blog, slug=slug)

    context = {
        "post": post,
    }

    return render(request, "blog/check_yes_or_no.html", context)
