from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class UserViewSet(viewsets.ViewSet):
    queryset = User.objects.all()

    @action(detail=False, methods=['post'], url_path='login')
    def user_login(self, request):
        email = request.data.get('email')

        user = authenticate(email=email)

        if user:
            token = Token.objects.get(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)