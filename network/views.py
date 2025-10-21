from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post, Follow


def index(request):
    if request.method == 'POST':
        if request.user.is_authenticated :
            content_data = request.POST
            post = Post(
                creator = request.user,
                content = content_data,
            )
            post.save()
            return HttpResponseRedirect(reverse("index"))
    posts = Post.objects.all().order_by("-time")
    return render(request, "network/index.html",  {
        "posts": posts
    })

def profile(request, creator):
    creatordata = User.objects.get(username=creator)
    follow = Follow.objects.all().filter(follower=creatordata)
    followedby = Follow.objects.all().filter(followed=creatordata)
    posts = Post.objects.all().filter(creator=creatordata).order_by("-time")
    return render(request, "network/profile.html",  {
        "following": follow,
        "followers": followedby,
        "posts": posts
    })
    
@login_required
def following(request):
    following = User.objects.filter(followers__follower = request.user)
    posts = Post.objects.filter(creator__in=following).order_by("-time")
    pass

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
