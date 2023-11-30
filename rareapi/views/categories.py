from rest_framework import viewsets, status
from rest_framework import serializers
from rest_framework.response import Response
from rareapi.models import Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'label']

class CategoryViewSet(viewsets.ViewSet):

    def list(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category)
            return Response(serializer.data)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def create(self, request):
        label = request.data.get('label')

        # creating the actual post
        post = Category.objects.create(
            label=label
        )

        # For a future many to many, code can be placed here if needed

        serializer = CategorySerializer(post, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk=None):
        try:

            category = Category.objects.get(pk=pk)

          
            self.check_object_permissions(request, category)

            serializer = CategorySerializer(data=request.data)
            if serializer.is_valid():
                category.label = serializer.validated_data['label']
                category.save()

                serializer = CategorySerializer(category, context={'request': request})
                return Response(None, status.HTTP_204_NO_CONTENT)

            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)