from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import serializers
from rareapi.models import Post
from .categories import CategorySerializer

class PostSerializer(serializers.ModelSerializer):
    is_owner = serializers.SerializerMethodField()
    categories = CategorySerializer(many=True)
    
    def get_is_owner(self, obj):
        # Check if the authenticated user is the owner
        return self.context['request'].user == obj.user
    
    class Meta:
        model = Post
        fields = ['id', 'is_owner', 'user_id', 'categories', 'title', 'publication_date', 'image_url', 'content', 'approved']
 

class PostViewSet(viewsets.ViewSet):

    def list(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            post = Post.objects.get(pk=pk)
            serializer = PostSerializer(post, many=False, context={'request': request})
            return Response(serializer.data)

        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        # getting data from the client's JSON payload
        category = request.data.get('category')
        title = request.data.get('title')
        publication_date = request.data.get('publication_date')
        image_url = request.data.get('image_url')
        content = request.data.get('content')
        approved = request.data.get('approved')

        # creating the actual post
        post = Post.objects.create(
            user=request.user,
            category=category,
            title=title,
            publication_date=publication_date,
            image_url=image_url,
            content=content,
            approved=approved
            )

        # For a future many to many, code can be placed here if needed
      

        serializer = PostSerializer(post, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)