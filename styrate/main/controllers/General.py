from ..models import Follow,User

class GeneralController:
    def AccountInformation(request, userObject):
        tempObj = userObject
        # Finding whether the current user is the owner 
        tempObj.isEqual = True if request.user.is_authenticated and request.user.id==userObject.id else False
        tempObj.following = True if request.user.is_authenticated and Follow.objects.filter(followFromUser_Key=User.objects.get(id=request.user.id), followToUser_Key=userObject).exists()else False
        # tempObj.follow_object_id = Follow.objects.get(followFromUser_Key=User.objects.get(id=request.user.id), followToUser_Key=userObject).id if tempObj.following else None
        return tempObj