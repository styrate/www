from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

# Change filename
class ChangeName:
    def userImage(instance, filename):
        ext = filename.split('.')[-1]
        filename_start = filename.replace('.'+ext,'')
        filename = "%s__%s.%s" % (uuid.uuid4(),filename_start, ext)
        return 'profileImage/' + filename
    def reviewImage(instance,filename):
        ext = filename.split('.')[-1]
        filename_start = filename.replace('.'+ext,'')
        filename = "%s__%s.%s" % (uuid.uuid4(),filename_start, ext)
        return 'profileImage/' + filename
# Models
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True, auto_created=True, blank=True)
    bioText = models.CharField(max_length=200, editable=True, blank=True, null=True)
    image = models.ImageField(editable=True, blank=True, null=True, upload_to=ChangeName.userImage)
    ranking = models.IntegerField(editable=True, null=True, blank=True)
    likeCount = models.IntegerField(editable=True, null=True, blank=True)
    pass

class Review(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    dateCreated = models.DateTimeField(auto_now_add=True, editable=True)
    title = models.CharField(max_length=100, editable=True, null=True)
    overview = models.CharField(max_length=100, editable=True, null=True)
    textField = models.CharField(max_length=1000, editable=True, blank=True, null=True)
    itemCategory = models.CharField(max_length=20, editable=True, null=True)
    image = models.ImageField(editable=True, blank=True, null=True, upload_to=ChangeName.reviewImage)
    videoID = models.CharField(max_length=100, editable=True)
    videoIsYT = models.BooleanField(auto_created=False, editable=True, null=True, blank=True)
    productName = models.CharField(max_length=25, editable=True, null=True)
    itemLink = models.CharField(max_length=150, editable=True, null=True)
    rating = models.IntegerField(editable=True, auto_created=0)
    likeCount = models.IntegerField(editable=True, null=True, blank=True)
    createdByUser_Key = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ReviewsCreatedBy_List')

class Follow(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    dateCreated = models.DateTimeField(auto_now_add=True, editable=True)
    followFromUser_Key = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Follows_List')
    followToUser_Key = models.ForeignKey(User, on_delete=models.CASCADE, related_name='FollowedBy_List')

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    dateCreated = models.DateTimeField(auto_now_add=True, editable=True)
    textField = models.CharField(max_length=300, editable=True, blank=True, null=True)
    createdByUser_Key = models.ForeignKey(User, on_delete=models.CASCADE, related_name='CommentsOfUser_List')
    onReview_Key = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='CommentsOfPost_List')

class Like(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    dateCreated = models.DateTimeField(auto_now_add=True, editable=True)
    createdByUser_Key = models.ForeignKey(User, on_delete=models.CASCADE, related_name='LikesOfUser_List')
    onReview_Key = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='LikesOfPost_List')
