from django.db import models
from django.contrib.auth.models import User

class Play(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    story_id = models.IntegerField()
    ending_page_id = models.IntegerField()
    ending_label = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Play {self.id} - Story {self.story_id}"

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('reader', 'Reader'),
        ('author', 'Author'),
        ('admin', 'Admin'),
    ]
 
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='reader')

    def __str__(self):
        return f"{self.user.username} - {self.role}"