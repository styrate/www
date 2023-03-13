from ..models import Like, User
import time
class LikeController:

    def AddLikeData(request, objectList, object):
        if(object):
            # Getting the like count
            tempObj = object
            tempObj.likeCount = len(Like.objects.filter(onReview_Key = tempObj))
            # Checking whether the user has liked the post
            if request.user.is_authenticated:
                tempObj.userLiked = True if Like.objects.filter(onReview_Key=tempObj, createdByUser_Key=request.user.id) else False
            return tempObj
        elif(objectList):
            tempObjList = objectList
            for tempObj in tempObjList:
                # Getting the like count
                tempObj = object
                tempObj.likeCount = len(Like.objects.filter(onReview_Key = tempObj))
                # Checking whether the user has liked the post
                if request.user.is_authenticated:
                    tempObj.userLiked = True if Like.objects.filter(onReview_Key=tempObj, createdByUser_Key=request.user.id) else False
            return tempObjList
        
    def calculateLeaderboard():
        allUserObjects = User.objects.all()
        userObject_and_likeCount_list = [] #2d array
        for userObject in allUserObjects:
            users_ReviewObjects = userObject.ReviewsCreatedBy_List.all()
            users_likeCount  = len(Like.objects.filter(onReview_Key__in = users_ReviewObjects))
            userObject_and_likeCount_list.append([userObject, users_likeCount])
        # sorts the 2d array in terms of its second column
        ranked_userObject_and_likeCount_list = sorted(userObject_and_likeCount_list,key=lambda l:l[1], reverse=True)
        count = 1
        for userObject_and_likeCount in ranked_userObject_and_likeCount_list:
            [userObject, likeCount] = userObject_and_likeCount
            userObject.ranking = count
            userObject.likeCount = likeCount
            userObject.save()
            count += 1

        