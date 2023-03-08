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
    return render(request, 'main/Home/home.html', {'reviewObjects': reviewObjects})

def renderAccountPage(request):
    return render(request, 'main/Account/Account.html')

def renderReviewPage(request, reviewID):
    # Currently UUIDs are int so will be converting str to int.
    reviewObject = Review.objects.get(id=int(reviewID))
    # Getting the Like Count
    ALTERED_reviewObject = LikeController.AddLikeData(request, object=reviewObject, objectList=None)
    return render(request, 'main/Review/review.html', {'data': ALTERED_reviewObject})