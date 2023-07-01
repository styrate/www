import urllib3
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
from django.db.models import Q


def renderLanding(request):
    payload = {
        'pageTitle': 'Styrate',
    }

    return render(request, 'main/landing/index.html', payload)

#  new-branch
def renderShowdown(request):
    

    videos = Review.objects.all().order_by("likeCountVideo")[::-1][:3]
    payload = {
        'pageTitle': 'Styrate - Showdown',
        "review": videos
    }
    
    return render(request, 'main/showdown/index.html', payload)


# main
def renderIndex(request):
    # Getting filter params
    searchValue = request.GET.get('search', None)
    categoryValue = request.GET.get('category', 'all')  # all, tech, misc, fashion, beauty
    sortValue = request.GET.get('sort', 'newest') # newest, oldest, lessLikes, moreLikes
    followedValue = request.GET.get('followed', 'all') # all, followed
    if searchValue=='':
        searchValue=None
    #Converting the filter params to usable django commands. 
    if sortValue=='newest': sortQuery = '-dateCreated'
    elif sortValue == 'oldest': sortQuery = 'dateCreated'
    elif sortValue == 'lessLikes': sortQuery = 'likeCount'
    elif sortValue == 'moreLikes': sortQuery = '-likeCount'
    # Full text search
    if searchValue==None:
        reviewObjects = Review.objects.all()
    else:
        reviewObjects = Review.objects.filter(Q(title__icontains=searchValue) | Q(productName__icontains=searchValue))
    # Filtering by category
    if categoryValue!='all':
        reviewObjects = reviewObjects.filter(itemCategory=categoryValue)
    # Sorting
    reviewObjects = reviewObjects.order_by(sortQuery)
    # Filtering by followed
    if followedValue=='followed' and request.user.is_authenticated:
        followObjectsFromUser = request.user.Follows_List.all()
        followingUsers = User.objects.filter(id__in =followObjectsFromUser.values('followToUser_Key') )
        reviewObjects = reviewObjects.filter(createdByUser_Key__in=followingUsers)
    # Get like data
    ALTERED_reviewObjects = LikeController.AddLikeData(request=request, objectList=reviewObjects, object=None)
    payload = {
        'pageTitle': 'Styrate - Product Reviews',
        'reviewObjects': ALTERED_reviewObjects, 
        'search': searchValue,
        'category': categoryValue,
        'sort': sortValue,
        'followed': followedValue,
    }
    
    return render(request, 'main/Home/home.html', payload)


def renderReviewPage(request, reviewID):
    reviewObject = Review.objects.get(id=reviewID)
    # Getting the comment list
    commentObjects = Comment.objects.filter(onReview_Key=reviewObject).order_by('-dateCreated')
    # Getting the embedded video data
    # tikTokVideoData = requests.get('https://www.tiktok.com/oembed?url='+ALTERED_reviewObject.videoID)
    # Checking if the user liked the review
    ALTERED_reviewObject = LikeController.AddLikeData(request=request, object=reviewObject, objectList=None)
    payload = {
        'pageTitle': ALTERED_reviewObject.title,
        'reviewObject': ALTERED_reviewObject,
        'commentObjects': commentObjects,
    }
    
    return render(request, 'main/Review/review.html', payload)

def isVideoLiked(request, review: Review):
    if LikeVideo.objects.filter(
        onReview_Key=review, createdByUser_Key=request.user.id):
        return True
    return False

def isVideoDisLiked(request, review):
    
    if DisLike.objects.filter(
        onReview_Key=review.id, createdByUser_Key=request.user.id):
        return True
    return False
def renderSubmitted(request):
    reviews = Review.objects.all().order_by("likeCountVideo" ,"disLikeCount")[::-1]
    for review in reviews:
        if isVideoDisLiked(request=request, review=review):
            review.userDisLiked = True
        else:
            review.userDisLiked = False
        if isVideoLiked(request=request, review=review):
            review.userLiked = True
        else:
            review.userLiked = False
        print(review.likeCountVideo)
        
        
    print("Here")
    payload = {
        "reviews": reviews
    }
    return render(request, "main/showdown/submitted.html", payload)

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
            payload = {'success': False}
    else:
        payload = {'success': False}
    return JsonResponse(payload)

def newReview(request):
    if(request.user.is_authenticated):
        isYT = request.POST.get('isYT', False)
        if isYT=='on': isYT=True
        if request.method == "POST": 
            
            try:
                newReview = Review(
                    title = request.POST["reviewTitle"],
                    # productName = request.POST["reviewProductName"],
                    rating = request.POST["reviewRating"],
                    createdByUser_Key = User.objects.get(id=request.user.id),
                    itemCategory = request.POST["reviewCategory"],
                    textField = request.POST["reviewBody"],
                    overview = request.POST["reviewOverview"],
                    itemLink = request.POST["reviewProductLink"],
                    videoID = request.POST["reviewVideoID"],
                    image = request.FILES['reviewImage'],
                    videoIsYT = isYT,
                    likeCount = 0
                )
                print(newReview.image)
                newReview.save()
                print("saved!")
                return redirect('/review/'+str(newReview.id))
            except Exception as e:
                payload = {
                    'pageTitle': 'Create - Error',
                }
                
                return render(request, "main/showdown/newreview.html", {'errorMessage': e})
            
    else: 
        return redirect('/login')
    return render(request, "main/showdown/newreview.html")

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
        pass

def likeControl(request):
    if request.user.is_authenticated:
        print(request.user)
        userLiked = request.POST.get('userLiked')
        if userLiked=='False' or userLiked=='false' or userLiked==False:
            Like(createdByUser_Key=User.objects.get(id=request.user.id), onReview_Key=Review.objects.get(id=request.POST.get('reviewID'))).save()
        else:
            Like.objects.filter(createdByUser_Key=User.objects.get(id=request.user.id), onReview_Key=Review.objects.get(id=request.POST.get('reviewID'))).delete()
        # After adding and removing the like, the rankings will be recalculated. This will occur on a second thread for efficiency.
        Thread(target=LikeController.calculateLeaderboard, args=()).start()
        # Chnaging post like count
        reviewObject = Review.objects.get(id=request.POST.get('reviewID'))
        likeCountOnObject = len(Like.objects.filter(onReview_Key=Review.objects.get(id=request.POST.get('reviewID'))))
        reviewObject.likeCount = likeCountOnObject
        reviewObject.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})
    
def like_video(request):
    if request.user.is_authenticated:
        
        userLiked = request.POST.get("userLiked")
        vals = ["False", "false", False]
        if userLiked in vals:
            
            LikeVideo(createdByUser_Key=User.objects.get(id=request.user.id), 
                    onReview_Key=Review.objects.get(id=request.POST.get('reviewID'))
                    ).save()  
        else:
            LikeVideo.objects.filter(createdByUser_Key=User.objects.get(id=request.user.id),
                                   onReview_Key=Review.objects.get(id=request.POST.get('reviewID')),
                                   ).delete()
        review = Review.objects.get(id=request.POST.get("reviewID"))
        LikeCountOnObject = len(LikeVideo.objects.filter(
            onReview_Key=Review.objects.get(id=request.POST.get("reviewID"))))
        review.likeCountVideo = LikeCountOnObject
        review.save()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False})
def disLikeControl(request):
    
    if request.user.is_authenticated:
        
        userDisLiked = request.POST.get("userDisLiked")
        vals = ["False", "false", False]
        if userDisLiked in vals:
            DisLike(createdByUser_Key=User.objects.get(id=request.user.id), 
                    onReview_Key=Review.objects.get(id=request.POST.get('reviewID')),
                    ).save()  
        else:
            DisLike.objects.filter(createdByUser_Key=User.objects.get(id=request.user.id),
                                   onReview_Key=Review.objects.get(id=request.POST.get('reviewID')),
                                   ).delete()
        review = Review.objects.get(id=request.POST.get("reviewID"))
        disLikeCountOnObject = len(DisLike.objects.filter(
            onReview_Key=Review.objects.get(id=request.POST.get("reviewID"))))
        review.disLikeCount = disLikeCountOnObject
        review.save()
        return JsonResponse({"success": True})
    
    return JsonResponse({"success": False})

def editProfile(reqeust):
    try:
        if reqeust.user.is_authenticated:
            # get data from reqeust
            username = reqeust.POST.get('username')
            about = reqeust.POST.get('about')
            image = reqeust.FILES.get('image')
            userObject = User.objects.get(id=reqeust.user.id)
            userObject.username = username
            userObject.bioText = about
            if image!=None:
                userObject.image = image
            userObject.save()
            return JsonResponse({'success': True})
        else:
            return redirect('/login')
    except Exception as e:
        return JsonResponse({'success': False})
    
@csrf_exempt
def getReviews(request):
    # JSON request and response
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')

        try:
            body = json.loads(body_unicode)
        except:
            return JsonResponse({'success': False})
        
        # Make sure the request contains a username
        if 'id' not in body:
            return JsonResponse({'success': False})
        
        # Get the reviews of said user (limit 6)
        reviews = Review.objects.filter(createdByUser_Key=User.objects.get(id=body['id'])).order_by('-dateCreated')[:6]

        # Create a list of reviews
        reviewList = []
        for review in reviews:
            reviewList.append({
                'id': review.id,
                'title': review.title,
                'productName': review.productName,
                'rating': review.rating,
                'createdByUser_Key': review.createdByUser_Key.id,
                'itemCategory': review.itemCategory,
                'textField': review.textField,
                'overview': review.overview,
                'itemLink': review.itemLink,
                'videoID': review.videoID,
                'image': review.image.url,
                'videoIsYT': review.videoIsYT,
                'likeCount': review.likeCount,
                'createdOn': review.dateCreated,
            })
        return JsonResponse({'success': True, 'reviews': reviewList})
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