from django.db import models
from django.contrib.auth.models import User

class Request(models.Model):
    sender = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[('paid', 'Paid'), ('declined', 'Declined'), ('pending', 'Pending')])

    def __str__(self):
        return f"Request from {self.sender.username} to {self.receiver.username}"





