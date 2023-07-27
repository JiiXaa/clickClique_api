from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ProfileSerializer
from .models import Profile


class ProfileList(APIView):
    def get(self, request):
        profiles = Profile.objects.all()
        data = ProfileSerializer(profiles, many=True).data
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

    def get_object(self, pk):
        try:
            profile = Profile.objects.get(pk=pk)
            return profile
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        profile = self.get_object(pk)
        data = ProfileSerializer(profile).data
        return Response(data)

    def put(self, request, pk):
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_404_BAD_REQUEST)
