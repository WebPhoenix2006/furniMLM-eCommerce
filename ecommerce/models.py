from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # This links Profile to User
    email = models.EmailField(unique=True)
    referral = models.CharField(max_length=50, blank=True, null=True)  # Optional field
    position = models.CharField(max_length=10, choices=[('Left', 'Left'), ('Right', 'Right')])
    password = models.CharField(max_length=128)  # Store hashed passwords for security
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.user.username  # Access the username through the user
