from django.contrib import admin
from .models import * 

admin.site.register([User, Review, Follow, Comment, Like])