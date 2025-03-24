from django.db import models

# Create your models here.

class UserDetails(models.Model):
    user_id = models.CharField(max_length=10, unique=True, primary_key=True)
    name = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=10)
    password = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)  # Set only on creation
    updated_at = models.DateTimeField(auto_now=True)      # Update on every save

    def __str__(self):
        return self.name 
    @property
    def is_authenticated(self):
        """Required for Django authentication"""
        return True

class BlogPost(models.Model):
    user = models.ForeignKey(UserDetails, on_delete=models.CASCADE,null=True, blank=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=50, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)      

    def __str__(self):
        return self.title