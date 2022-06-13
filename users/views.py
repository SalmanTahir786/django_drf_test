from .models import UserProfile
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import UserProfileSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer