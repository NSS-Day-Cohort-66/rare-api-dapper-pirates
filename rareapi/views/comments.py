from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from rareapi.models import Comment


# class CommentViewSet(viewsets.Viewset):

#     def list(self, request):

#         comments = Comment.objects.all()
