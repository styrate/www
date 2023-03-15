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
from .controllers.General import GeneralController
from django.core.files import File
import os
from threading import Thread

def renderIndex(request):
    # pageNumber = int(request.GET.get('page', '1'))
    # numPerPage = 9
    # reviewObjects = Review.objects.all().order_by('-dateCreated')[(pageNumber-1)*numPerPage : (pageNumber)*numPerPage]
    # nextPageURL = '/?page='+str(pageNumber+1)
    # prevPageURL = '/?page='+str(pageNumber-1)
    reviewObjects = Review.objects.all().order_by('-dateCreated')
    ALTERED_reviewObjects = LikeController.AddLikeData(object=None, objectList=reviewObjects, request=request)
    payload = {
        'pageTitle': 'Styrate - Product Reviews',
        'reviewObjects': ALTERED_reviewObjects,
        # 'pageNumber': pageNumber,
        # 'pagination': {
        #     'nextPageURL':nextPageURL,
        #     'displayNext': True,
        #     'prevPageURL': prevPageURL,
        #     'displayPrev': True if not (pageNumber==1) else False 
        # }
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
        ALTERED_userObject = GeneralController.AccountInformation(request=request, userObject=userObject)
        payload = {
            'pageTitle': 'Account | '+userObject.username,
            'userObject': ALTERED_userObject
        }
        return render(request, 'main/Account/Account.html', payload)
    
    else:
        return redirect('/404')
    
def renderTop(request):
    userObjects = User.objects.all().order_by('ranking')
    payload = {
        'pageTitle': 'User Rankings',
        'userObjects': userObjects
    }
    return render(request, 'main/Top/top.html', payload)

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

def followHandler(request):
    try:
        if request.user.is_authenticated:
            isRemove = request.POST.get("isRemove")
            followFromUser_Key = User.objects.get(id=request.user.id)
            followToUser_Key = User.objects.get(id=request.POST.get("followTo_ID"))
            if isRemove=='True':
                followObject = Follow.objects.get(followFromUser_Key=followFromUser_Key, followToUser_Key=followToUser_Key).delete()
                return redirect(request.META['HTTP_REFERER'])
            else:
                Follow(followFromUser_Key=followFromUser_Key, followToUser_Key=followToUser_Key).save()
                return redirect(request.META['HTTP_REFERER'])
    except Exception as e:
        print(e)

def likeControl(request):
    if request.user.is_authenticated:
        userLiked = request.POST.get('userLiked')
        if userLiked=='False' or userLiked=='false' or userLiked==False:
            Like(createdByUser_Key=User.objects.get(id=request.user.id), onReview_Key=Review.objects.get(id=request.POST.get('reviewID'))).save()
        else:
            Like.objects.filter(createdByUser_Key=User.objects.get(id=request.user.id), onReview_Key=Review.objects.get(id=request.POST.get('reviewID'))).delete()
        # After adding and removing the like, the rankings will be recalculated. This will occur on a second thread for efficiency.
        Thread(target=LikeController.calculateLeaderboard, args=()).start()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})

    
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
            image='default/user.png',
            likeCount = 0,
        )
        newUser.save()
        login(request, newUser)
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

def deleteUser(request):
    if request.user.is_authenticated and request.POST.get('userID')==str(request.user.id):
        userObj = User.objects.get(id=request.user.id)
        userObj.delete()
        logout(request)
        return redirect('/')
    return redirect('/')
