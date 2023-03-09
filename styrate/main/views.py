from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import *
import json
from django.core import serializers
from .controllers.LikeController import LikeController

def renderIndex(request):
    reviewObjects = Review.objects.all()
    payload = {
        'pageTitle': 'Styrate - Product Reviews',
        'reviewObjects': reviewObjects
    }
    return render(request, 'main/Home/home.html', payload)

def renderAccountPage(request):
    payload = {
        'pageTitle': 'Account',
    }
    return render(request, 'main/Account/Account.html', payload)

def renderReviewPage(request, reviewID):
    reviewObject = Review.objects.get(id=reviewID)
    # Getting the Like Count
    ALTERED_reviewObject = LikeController.AddLikeData(request, object=reviewObject, objectList=None)
    payload = {
        'pageTitle': ALTERED_reviewObject.title,
        'reviewObject': ALTERED_reviewObject
    }
    return render(request, 'main/Review/review.html', payload)