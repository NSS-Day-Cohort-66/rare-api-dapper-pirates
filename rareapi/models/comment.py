from django.db import models
from django.contrib.auth.models import User


class Comment(models.Model):
    book = models.ForeignKey(
        "Post", on_delete=models.CASCADE, related_name='comments')
    commenter = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_post')
    created_on = models.DateField(auto_now_add=True)
    content = models.CharField(max_length=1000)
