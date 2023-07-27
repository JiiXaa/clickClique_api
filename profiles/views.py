from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import ProfileSerializer
from .models import Profile
from cc_api.permissions import IsOwnerOrReadOnly


class ProfileList(APIView):
    def get(self, request):
        profiles = Profile.objects.all()
        data = ProfileSerializer(profiles, many=True, context={"request": request}).data
        return Response(data)

    def post(self, request):
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class ProfileDetail(APIView):
    # serializer_class set to ProfileSerializer renders form with pre-populated fields in the template instead of RAW data
    serializer_class = ProfileSerializer
    # permission_classes set to IsOwnerOrReadOnly to allow only the owner of the profile to edit it
    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self, pk):
        try:
            profile = Profile.objects.get(pk=pk)
            # This line checks if the user is the owner of the profile
            self.check_object_permissions(self.request, profile)
            return profile
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        profile = self.get_object(pk)
        data = ProfileSerializer(profile, context={"request": request}).data
        return Response(data)

    def put(self, request, pk):
        profile = self.get_object(pk)
        serializer = ProfileSerializer(
            profile, data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_404_BAD_REQUEST)
