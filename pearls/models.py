from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=128, null=False, blank=False)
    description = models.TextField(null=False, blank=True, default='')
    created_at = models.DateTimeField(auto_now=True, null=False, blank=False)
    author = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1)

    class Meta:
        ordering = ['-created_at']
