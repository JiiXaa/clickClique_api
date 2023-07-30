from django.http import Http404
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post
from .serializers import PostSerializer
from cc_api.permissions import IsOwnerOrReadOnly


class PostList(APIView):
    # To have a nice input form in the template, we need to set the serializer_class to PostSerializer
    serializer_class = PostSerializer
    # Make sure user is authenticated before posting, no post form will be rendered if user is not authenticated
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetail(APIView):
    # To have a nice input form in the template, we need to set the serializer_class to PostSerializer
    serializer_class = PostSerializer
    # permission_classes set to IsOwnerOrReadOnly to allow only the owner of the post to edit it
    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self, pk):
        try:
            post = Post.objects.get(pk=pk)
            # This line checks if the user is the owner of the post
            self.check_object_permissions(self.request, post)
            return post
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(post, context={"request": request})
        return Response(serializer.data)

    def put(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(
            post, data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_404_BAD_REQUEST)

    def delete(self, request, pk):
        post = self.get_object(pk)
        post.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
