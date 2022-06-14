from rest_framework import generics
from rest_framework import viewsets, permissions, authentication, status
from rest_framework.response import Response

from .models import UserProfile, Post, User
from .serializers import UserProfileSerializer, PostSerializer, RegisterSerializer, UserSerializer


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

    def update_user_userprofile(self, request, *args, **kwargs):
        import pdb;
        pdb.set_trace()
        given_data = request.data
        instance = self.get_object()
        profile_serializer = self.serializer_class(instance, data=given_data, partial=True)
        profile_serializer.is_valid(raise_exception=True)
        self.perform_update(profile_serializer)
        user_id = instance.email.id
        get_user = User.objects.filter(id=user_id)
        user_serializer = UserSerializer(get_user.first(), data=given_data, partial=True)
        user_serializer.is_valid(raise_exception=True)
        self.perform_update(user_serializer)
        return Response({
            'message': 'user and user_profile both models update successfully',
            'data': {
                'user_data': user_serializer.data,
                'user_profile': profile_serializer.data
            }
        }, status=status.HTTP_200_OK)


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


class PostAnonymousViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_anonymous_post(self, request):
        get_all_post = Post.objects.all()
        serializer = PostSerializer(get_all_post, many=True)
        return Response({
            "message": "shown all posts data for anonymous user",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
