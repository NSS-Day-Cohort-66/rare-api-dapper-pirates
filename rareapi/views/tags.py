from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import serializers
from rareapi.models import Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'label']


class TagViewSet(viewsets.ViewSet):

    def list(self, request):
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        try:
            tag =Tag.objects.get(pk=pk)
            serializer = TagSerializer(tag)
            return Response(serializer.data)
        except Tag.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        

    def create(self, request):
        label = request.data.get('label')

        # creating the actual post
        tag = Tag.objects.create(
            label=label
        )

        # For a future many to many, code can be placed here if needed

        serializer = TagSerializer(tag, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)