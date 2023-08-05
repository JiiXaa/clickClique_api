from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, filters
from cc_api.permissions import IsOwnerOrReadOnly
from .models import Post
from .serializers import PostSerializer


class PostList(generics.ListCreateAPIView):
    """
    List posts or create a post if logged in
    The perform_create method associates the post with the logged in user.
    """

    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Post.objects.annotate(
        comments_count=Count("owner__comment", distinct=True),
        likes_count=Count("owner__like", distinct=True),
    ).order_by("-created_at")
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    # id is not needed as it is the default ordering field
    filterset_fields = [
        # show user feed posts searching by who is following user posts.
        "owner__followed__owner__profile",
        # show user liked posts
        "likes__owner__profile",
        # show user posts
        "owner__profile",
    ]
    search_fields = [
        "owner__username",
        "title",
    ]
    ordering_fields = [
        "likes_count",
        "comments_count",
        "likes__created_at",
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve a post and edit or delete it if you own it.
    """

    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Post.objects.annotate(
        comments_count=Count("owner__comment", distinct=True),
        likes_count=Count("owner__like", distinct=True),
    ).order_by("-created_at")
