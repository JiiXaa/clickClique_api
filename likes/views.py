from rest_framework import generics, permissions
from cc_api.permissions import IsOwnerOrReadOnly
from .models import Like
from .serializers import LikeSerializer


class LikeList(generics.ListCreateAPIView):
    """
    List all likes, or create a new like.
    """

    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Like.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LikeDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a like instance.
    """

    serializer_class = LikeSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Like.objects.all()
