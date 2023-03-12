from ..models import *

class GeneralController:
    def AccountInformation(request, userObject):
        tempObj = userObject
        # Finding whether the current user is the owner 
        tempObj.isEqual = True if request.user.is_authenticated and request.user.id==userObject.id else False
        # Finding whether the user follows them
        tempObj.following = True if request.user.is_authenticated and Follow.objects.filter(followFromUser_Key=User.objects.get(id=request.user.id), followToUser_Key=userObject).exists()else False
        # Finding whether user's stats
        tempObj.numReviews = len(userObject.ReviewsCreatedBy_List.all())
        tempObj.numFollowers = len(userObject.FollowedBy_List.all())
        tempObj.numFollowing = len(userObject.Follows_List.all())
        # Finding the number of likes
        users_ReviewObjects = userObject.ReviewsCreatedBy_List.all()
        tempObj.likeCount  = len(Like.objects.filter(onReview_Key__in = users_ReviewObjects))
        return tempObj