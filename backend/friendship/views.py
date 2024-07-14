from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

# models 
from accounts.models import User
from .models import Friendship, FriendRequest

# Create your views here.



# for sending friends requests 
class SendFriendRequest(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        receiver_id = request.data.get('receiver_id')
        try:
            receiver = User.objects.get(id=receiver_id)
        except:
            return Response({"message":"User not exists"},
                             status=status.HTTP_400_BAD_REQUEST)
        if FriendRequest.can_send_request(request.user):
            FriendRequest.objects.create(sender=request.user, receiver=receiver)
            return Response ({"message":"Friend request sent."},
                              status=status.HTTP_201_CREATED)
        else:
            return Response({"message":"You have sent too many friend requests, Please wait a while before sending more"},
                            status=status.HTTP_429_TOO_MANY_REQUESTS)


# for accepting friends request 
class AcceptFriendRequest(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        try:
            request_id = request.data.get('request_id')
            friend_request = FriendRequest.objects.get(id=request_id, receiver=request.user)
        except:
            return Response({"message":"Friend request not found"}, 
                            status=status.HTTP_404_NOT_FOUND)
        friend_request.status = "accepted"
        friend_request.save()
        Friendship.objects.create(user1=friend_request.sender, user2=friend_request.receiver)
        return Response({"message":"Friend request accepted"}, 
                        status=status.HTTP_200_OK)
    

# rejecting friend request 
class RejectFriendRequest(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        try:
            request_id = request.data.get('request_id')
            friend_request = FriendRequest.objects.get(id=request_id, receiver=request.user)
        except:
            return Response({"message":"Friend request not found"}, 
                            status=status.HTTP_404_NOT_FOUND)
        friend_request.status = "rejected"
        friend_request.save()
        return Response({"message":"Friend request rejected"},
                         status=status.HTTP_200_OK)
    
        


# lists of pending friends request 

# lists of friends of a user 


