from ..models import Like

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