from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

# models 
from accounts.models import User
from .models import Friendship, FriendRequest

# serializers
from .serializers import FriendRequestSerializer

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
        
        # Check if a pending friend request already exists
        if FriendRequest.has_pending_request(sender=request.user, receiver=receiver): 
            return Response({"message":"There is already a pending friend request to this user"},
                            status=status.HTTP_403_FORBIDDEN)
        
        # Check if the sender can send a new request
        if FriendRequest.can_send_request(request.user):
            FriendRequest.objects.create(sender=request.user, receiver=receiver)
            return Response ({"message":"Friend request sent."},
                            status=status.HTTP_201_CREATED) 
        else:
            return Response({
            "message":"You have sent too many friend requests, Please wait a while before sending more"
            },status=status.HTTP_429_TOO_MANY_REQUESTS)


# for accepting friends request 
class AcceptFriendRequest(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
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
class PendingFriendsRequest(APIView):
    """
    View to list all pending friend requests for the authenticated user.
    """
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            pending_request = FriendRequest.objects.filter(receiver=request.user, status='pending')
            serializer = FriendRequestSerializer(pending_request, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            


# lists of friends of a user 


