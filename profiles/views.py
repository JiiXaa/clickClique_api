from django.db.models import Count
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import ProfileSerializer
from .models import Profile
from cc_api.permissions import IsOwnerOrReadOnly


class ProfileList(generics.ListAPIView):
    """
    List all profiles.
    No create view as profile creation is handled by django signals.
    """

    # annotate allows us to add extra fields to the queryset, in this case the number of posts for each profile. This is used in the template to display the number of posts for each profile.
    # distinct=True is used to avoid counting the same post twice if it has more than one comment.
    # owner__posts: owner is the foreign key in the Post model, post is the related name.
    # Need to add all annotated fields to the ProfileSerializer as read_only fields. Otherwise, the serializer will try to validate them.
    queryset = Profile.objects.annotate(
        posts_count=Count("owner__post", distinct=True),
        followers_count=Count("owner__followed", distinct=True),
        following_count=Count("owner__following", distinct=True),
    ).order_by("-created_at")
    serializer_class = ProfileSerializer
    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = [
        "owner__following__followed__profile",
    ]
    ordering_fields = [
        "posts_count",
        "followers_count",
        "following_count",
        "owner__followings__created_at",
        "owner__followed__created_at",
    ]


class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve or update a profile if you are the owner.
    """

    # serializer_class set to ProfileSerializer renders form with pre-populated fields in the template instead of RAW data
    serializer_class = ProfileSerializer
    # permission_classes set to IsOwnerOrReadOnly to allow only the owner of the profile to edit it
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Profile.objects.annotate(
        posts_count=Count("owner__post", distinct=True),
        followers_count=Count("owner__followed", distinct=True),
        following_count=Count("owner__following", distinct=True),
    ).order_by("-created_at")
