from rest_framework import generics
from .serializers import ProfileSerializer
from .models import Profile
from cc_api.permissions import IsOwnerOrReadOnly


class ProfileList(generics.ListAPIView):
    """
    List all profiles.
    No create view as profile creation is handled by django signals.
    """

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve or update a profile if you are the owner.
    """

    # serializer_class set to ProfileSerializer renders form with pre-populated fields in the template instead of RAW data
    serializer_class = ProfileSerializer
    # permission_classes set to IsOwnerOrReadOnly to allow only the owner of the profile to edit it
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Profile.objects.all()
