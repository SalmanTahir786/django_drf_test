from rest_framework import viewsets, permissions, authentication, status
from rest_framework.response import Response

from .models import UserProfile, Post
from .serializers import UserProfileSerializer, PostSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def update(self, request, *args, **kwargs):
        # import pdb;
        # pdb.set_trace()
        instance = self.get_object()
        given_date = request.data
        serializer = self.serializer_class(instance, data=given_date, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            'message': 'user profile updated successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)


class PostViewSet(viewsets.ModelViewSet):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def update(self, request, *args, **kwargs):
        import pdb;
        pdb.set_trace()
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

