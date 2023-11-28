from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from rareapi.models import Comment, Post


class CommentSerializer(serializers.ModelSerializer):
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'is_owner', 'post',
                  'commenter', 'content', 'created_on']
        read_only_fields = ['commenter']

    def get_is_owner(self, obj):

        return self.context['request'].user == obj.commenter


class CommentViewSet(viewsets.ViewSet):

    def list(self, request):

        comments = Comment.objects.all()

        serializer = CommentSerializer(
            comments, many=True, context={'request': request}
        )

        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        try:
            comment = Comment.objects.get(pk=pk)
            serializer = CommentSerializer(
                comment, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        post_commented = Post.objects.get(pk=request.data['postId'])
        comment = Comment()
        comment.commenter = request.user
        comment.post = post_commented
        comment.content = request.data['content']
        comment.created_on = comment.created_on
        comment.save()

        try:
            serialized = CommentSerializer(
                comment, many=False, context={'request': request})
            return Response(serialized.data, status=status.HTTP_201_CREATED
                            )
        except Exception:
            return Response(None, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            comment = Comment.objects.get(pk=pk)

            if comment.commenter.id != request.user.id:
                return Response(status=status.HTTP_403_FORBIDDEN)

            comment.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
