from rest_framework import generics
from rest_framework import viewsets, permissions, authentication, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import UserProfile, Post, User
from .serializers import UserProfileSerializer, PostSerializer, RegisterSerializer, UserSerializer


class UserDetailAPI(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data)


# Class based view to register user
class RegisterUserAPIView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        given_date = request.data
        serializer = self.serializer_class(instance, data=given_date, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            'message': 'user profile updated successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    # def login_user(self, request):
    #     import pdb;
    #     pdb.set_trace()
    #     given_data = request.data
    #     # user = User.objects.filter(email=given_data['username'], password=given_data['password'])
    #     user = User.objects.get(email="salman@gmail.com", password="admin")
    #     "ok"


class PostViewSet(viewsets.ModelViewSet):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        given_data = request.data
        instance_id = instance.author.id
        given_author_id = given_data['author']
        if str(instance_id) == given_author_id:
            serializer = self.serializer_class(instance, data=given_data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response({
                'message': 'user profile updated successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'message': 'you have no rights for edit',
            }, status=status.HTTP_400_BAD_REQUEST)
