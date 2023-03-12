from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import *
import json
from django.core import serializers
from .controllers.LikeController import LikeController
from django.core.files import File
import os

def renderIndex(request):
    reviewObjects = Review.objects.all().order_by('-dateCreated')
    payload = {
        'pageTitle': 'Styrate - Product Reviews',
        'reviewObjects': reviewObjects
    }
    return render(request, 'main/Home/home.html', payload)


def renderReviewPage(request, reviewID):
    reviewObject = Review.objects.get(id=reviewID)
    # Getting the Like Count
    ALTERED_reviewObject = LikeController.AddLikeData(request, object=reviewObject, objectList=None)
    # Getting the comment list
    commentObjects = Comment.objects.filter(onReview_Key=reviewObject).order_by('-dateCreated')
    payload = {
        'pageTitle': ALTERED_reviewObject.title,
        'reviewObject': ALTERED_reviewObject,
        'commentObjects': commentObjects
    }
    return render(request, 'main/Review/review.html', payload)

def renderlogIn(request):
    payload = {
        'pageTitle': 'Styrate Login',
        'login': True,
    }
    return render(request, 'main/Auth/auth.html', payload)

def renderRegister(request):
    payload = {
        'pageTitle': 'Join Styrate',
        'login': False,
    }
    return render(request, 'main/Auth/auth.html', payload)

def renderNewReview(request):
    payload = {
        'pageTitle': 'Write a review',
    }
    return render(request, 'main/New/new.html', payload)

def renderAccountPage(request, id):
    if User.objects.filter(id=id).exists():
        userObject = User.objects.get(id=id)
        payload = {
            'pageTitle': 'Account | '+userObject.username,
        }
        return render(request, 'main/Account/Account.html', payload)
    else:
        return redirect('/404')

# API
def newComment(request):
    if request.user.is_authenticated:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        try:
            createdByUserObject = User.objects.get(id=request.user.id)
            onReviewObject = Review.objects.get(id=body['reviewID'])
            Comment(textField=body['commentBody'], createdByUser_Key=createdByUserObject, onReview_Key=onReviewObject).save()
            payload = {'success': True}
        except Exception as e: 
            print(e)
            payload = {'success': False}
    else:
        print('No auth')
        payload = {'success': False}
    return JsonResponse(payload)

def newReview(request):
    if(request.user.is_authenticated):
        try:
            newReview = Review(
                title = request.POST["reviewTitle"],
                productName = request.POST["reviewProductName"],
                rating = request.POST["reviewRating"],
                createdByUser_Key = User.objects.get(id=request.user.id),
                itemCategory = request.POST["reviewCategory"],
                textField = request.POST["reviewBody"],
                overview = request.POST["reviewOverview"],
                itemLink = request.POST["reviewProductLink"],
                videoID = request.POST["reviewVideoID"],
                image = request.FILES['reviewImage']
            )
            newReview.save()
            return redirect('/review/'+str(newReview.id))
        except Exception as e:
            print(e)
            payload = {
                'pageTitle': 'Create - Error',
            }
            return render(request, 'main/New/new.html', {'errorMessage':e })
    else: 
        return redirect('/login')

# Auth
def logOut(request):   
    logout(request)
    return redirect('/')

def registerNewUser(request):
    payload = {
        'pageTitle': 'Join Styrate',
        'login': False,
    }
    try:
        # Checking whether the data
        if(request.POST.get('password')!=request.POST.get('repassword')):
            payload['error'] ='Passwords are not the same'
            return render(request, 'main/Auth/auth.html', payload)
        newUser = User.objects.create_user(
            username=request.POST.get('username'),
            email=request.POST.get('email'),
            password=request.POST.get('password'),
            bioText=f"Hi there. I'm a new user.",
            image='default/user.png'
        )
        newUser.save()
        user = authenticate(request=request, user=newUser)
        return redirect('/account/'+str(newUser.id))
    except Exception as e:
        payload['error'] = e
        return render(request, 'main/Auth/auth.html', payload)

def loginUser(request):
    payload = {
        'pageTitle': 'Styrate Login',
        'login': True,
    }
    try:
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            payload['error'] = 'Invalid username or password'
            return render(request, "main/Auth/auth.html", payload)
    except Exception as e:
        payload['error'] = e
        return render(request, 'main/Auth/auth.html', payload)