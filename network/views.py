from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator

from .models import User, Post, Follow


def index(request):
    if request.method == 'POST':
        if request.user.is_authenticated :
            content_data = request.POST.get("content", "").strip()
            if content_data != "":
                post = Post(
                    creator = request.user,
                    content = content_data,
                )
                post.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        posts_list = Post.objects.all().order_by("-time")
        paginator = Paginator(posts_list, 10)  # 10 posts por página
        page_number = request.GET.get("page")
        posts = paginator.get_page(page_number)
        return render(request, "network/index.html",  {
            "posts": posts
        })

def profile(request, creator):
    creatordata = User.objects.get(username=creator)
    if request.method == "POST":
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("login"))
        rel = Follow.objects.filter(follower=request.user,followed=creatordata)
        if rel.exists():
            rel.delete()
        else:
            Follow.objects.create(follower=request.user,followed=creatordata)
        return HttpResponseRedirect(reverse("profile", kwargs={"creator": creator}))
    is_following = False
    if request.user.is_authenticated:
        is_following = Follow.objects.filter(
            follower=request.user,
            followed=creatordata
        ).exists()
    follow = Follow.objects.all().filter(follower=creatordata)
    followedby = Follow.objects.all().filter(followed=creatordata)
    posts_list = Post.objects.filter(creator=creatordata).order_by("-time")
    paginator = Paginator(posts_list, 10)  # 10 posts por página
    page_number = request.GET.get("page")
    posts = paginator.get_page(page_number)
    
    return render(request, "network/profile.html",  {
        "creator": creatordata,
        "following": follow,
        "followers": followedby,
        "posts": posts,
        "is_following": is_following
    })

def edit_post(request, post_id):
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)

    post = Post.objects.get(id=post_id)

    if request.user != post.creator:
        return JsonResponse({"error": "Not authorized"}, status=403)

    data = json.loads(request.body)
    new_content = data.get("content", "").strip()

    if new_content == "":
        return JsonResponse({"error": "Content cannot be empty"}, status=400)

    post.content = new_content
    post.save()

    return JsonResponse({"message": "Post updated successfully", "content": new_content})


def toggle_like(request, post_id):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required"}, status=403)

    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required"}, status=400)

    post = Post.objects.get(id=post_id)

    # Se já curtiu → remove
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True

    return JsonResponse({
        "liked": liked,
        "like_count": post.likes.count()
    })

@login_required
def following(request):
    following = User.objects.filter(followers__follower = request.user)
    posts = Post.objects.filter(creator__in=following).order_by("-time")
    return render(request, "network/index.html",  {
        "posts": posts
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
