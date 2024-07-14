from django.db import models
from django.utils import timezone
from datetime import timedelta

# import models 
from accounts.models import User
# Create your models here.



REQUEST_STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('accepted', 'Accepted'),
    ('rejected', 'Rejected'),
)


class FriendRequest(models.Model):
    sender = models.ForeignKey(User, related_name='sent_friend_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='receive_friend_reqeusts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=REQUEST_STATUS_CHOICES, default='pending')

    class Meta:
        indexes = [
            models.Index(fields=[
                'created_at'
            ])
        ]


    # check if the user made more than 3 request within a minute
    @staticmethod
    def can_send_request(user):
        one_minute_ago = timezone.now() - timedelta(minutes=1)
        request_count = FriendRequest.objects.filter(sender=user, created_at__gte=one_minute_ago).count()
        return request_count < 3 
    

    '''
    check if the user1(sender) had already send a friend request to the user2(receiver) 
    and the current state is pending , in that case no need to send another request
    '''
    @staticmethod
    def has_pending_request(sender, receiver):
        return FriendRequest.objects.filter(
            sender=sender,
            receiver=receiver,
            status='pending'
        ).exists()

    
    def __str__(self):
        return f"{self.sender} to {self.receiver}"
    



class Friendship(models.Model):
    user1 = models.ForeignKey(User, related_name='friend1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='friend2', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta :
        unique_together = ('user1', 'user2')

    def __str__(self):
        return f"{self.user1} and {self.user2}"
    
    


    

