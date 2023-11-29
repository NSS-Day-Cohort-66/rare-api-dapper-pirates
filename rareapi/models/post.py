from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_post')
    category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name='post_category')
    title = models.CharField(max_length=155)
    publication_date = models.DateField(auto_now_add=True)
    image_url = models.CharField(max_length=200)
    content = models.CharField(max_length=155)
    approved = models.BooleanField(default=False)