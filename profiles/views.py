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
