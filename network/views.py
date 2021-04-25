from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core import serializers
from django.core.paginator import Paginator
from datetime import datetime
from django.utils.safestring import SafeString

from .models import User, Comment, Post, Profile, Like
import json


def index(request):

    return render(request, "network/index.html", {
        'user': request.user,
    })


def profile(request, profile):
    return render(request, "network/index.html", {
        "profile": profile
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


def get_current_user(request):
    user = request.user.serialize()
    return JsonResponse(user)


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

            profile = Profile(user=user)
            profile.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def get_posts_following(request):
    user = request.user
    userProfile = Profile.objects.get(user=user)
    following = list(userProfile.following.all())
    queryPosts = Post.objects.filter(
        poster__in=following).order_by('-timestamp').all()
    inList = []
    for post in queryPosts:
        inList.append(post.serialize())
    return JsonResponse(inList, safe=False)

# returns a profile object for a user


def get_user(request, username):
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)
    jsonProfile = profile.serialize()
    postsForUser = Post.objects.filter(
        poster=user).order_by('-timestamp').all()
    jsonPostsForUser = []
    for post in postsForUser:
        jsonPostsForUser.append(post.serialize())

    response = {
        'profile': jsonProfile,
        'postsForUser': jsonPostsForUser,
    }
    return JsonResponse(response)


def posts(request):
    # sort posts by reverse chronological order
    inList = []
    posts = Post.objects.order_by('-timestamp').all()

    for post in posts:
        inList.append(post.serialize())

    return JsonResponse(inList, safe=False)


def posts_for_user(request, username):
    user = User.objects.get(username=username)
    inList = []
    posts = Post.objects.filter(poster=user).order_by('-timestamp').all()

    for post in posts:
        inList.append(post.serialize())

    return JsonResponse(inList, safe=False)


def create(request, text):
    poster = request.user
    timestamp = datetime.now()
    post = Post(poster=poster, text=text, timestamp=timestamp, likes=0)
    post.save()

    return JsonResponse({})


# give like to a post
def like(request, id):
    try:
        post = Post.objects.get(id=id)
        post.likes = post.likes + 1
        post.save()
        like = Like(user=request.user, post=post)
        like.save()

        return JsonResponse({
            'message': f'succesfully liked post {id}',
            'post': post.serialize()
        })
    except:
        return JsonResponse({'message': f'failed to like post{id}'})

# give dislike to a post
def dislike(request, id):
    try:
        post = Post.objects.get(id=id)
        post.likes = post.likes - 1
        post.save()

        like = Like.objects.get(user=request.user, post=post)
        like.delete()

        return JsonResponse({
            'message': f'succesfully liked post {id}',
            'post': post.serialize()
        })
    except:
        return JsonResponse({'message': f'failed to dislike post{id}'})


def edit(request, id, content):
    post = Post.objects.get(id=id)
    post.text = content
    post.save()
    return JsonResponse({
        'message': 'Succesfully edited',
        'post': post.serialize()
    })


def follow(request, username):
    try:
        user = Profile.objects.get(user=request.user)
        userToFollow = User.objects.get(username=username)
        user.following.add(userToFollow)
        user.save()
        jsonUser = Profile.objects.get(user=userToFollow).serialize()
        return JsonResponse({
            'message': f'Succesfully followed {username}',
            'profile': jsonUser
        })
    except:
        return JsonResponse({'message': f'Failed to follow {username}'})


def unfollow(request, username):
    try:
        user = Profile.objects.get(user=request.user)
        userToUnfollow = User.objects.get(username=username)
        user.following.remove(userToUnfollow)
        user.save()
        jsonUser = Profile.objects.get(user=userToUnfollow).serialize()
        return JsonResponse({
            'message': f'Successfully unfollowed {username}',
            'profile': jsonUser
        })
    except:
        return JsonResponse({'message': f'Failed to unfollow {username}'})
