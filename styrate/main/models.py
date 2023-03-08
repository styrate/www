from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    bioText = models.CharField(max_length=100, editable=True, blank=True, null=True)
    image = models.ImageField(editable=True, blank=True, null=True)
    pass

class Review(models.Model):
    id = models.AutoField(primary_key=True, editable=True)
    dateCreated = models.DateTimeField(auto_now_add=True, editable=True)
    title = models.CharField(max_length=100, editable=True, null=True)
    overview = models.CharField(max_length=100, editable=True, null=True)
    textField = models.CharField(max_length=1000, editable=True, blank=True, null=True)
    itemCategory = models.CharField(max_length=20, editable=True, null=True)
    image = models.ImageField(editable=True, blank=True, null=True)
    videoID = models.CharField(max_length=100, editable=True)
    productName = models.CharField(max_length=25, editable=True, null=True)
    itemLink = models.CharField(max_length=150, editable=True, null=True)
    createdByUser_Key = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ReviewsCreatedBy_List')

class Follow(models.Model):
    id = models.AutoField(primary_key=True, editable=True)
    dateCreated = models.DateTimeField(auto_now_add=True, editable=True)
    followFromUser_Key = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Follows_List')
    followToUser_Key = models.ForeignKey(User, on_delete=models.CASCADE, related_name='FollowedBy_List')

class Comment(models.Model):
    id = models.AutoField(primary_key=True, editable=True)
    dateCreated = models.DateTimeField(auto_now_add=True, editable=True)
    textField = models.CharField(max_length=300, editable=True, blank=True, null=True)
    createdByUser_Key = models.ForeignKey(User, on_delete=models.CASCADE, related_name='CommentsOfUser_List')
    onReview_Key = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='CommentsOfPost_List')