from django.db import models

# defining tag class and creating fields
class Tag(models.Model):
    label = models.CharField(max_length=155)