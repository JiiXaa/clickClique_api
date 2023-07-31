from django.contrib.auth.models import User
from .models import Post
from rest_framework import status
from rest_framework.test import APITestCase


# class PostListViewTests(APITestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(
#             username="test_user", password="test_password"
#         )
#         self.client.login(username="test_user", password="test_password")

#     def test_create_post(self):
#         url = "/api/posts/"
#         data = {"title": "Test Post", "content": "Test Content"}
#         response = self.client.post(url, data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Post.objects.count(), 1)
#         self.assertEqual(Post.objects.get().title, "Test Post")

#     def test_get_posts(self):
#         url = "/api/posts/"
#         response = self.client.get(url, format="json")
#         self.assertEqual(response.status_code, status.HTTP_200_OK)


class PostListViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username="test_user", password="test_password")

    def test_can_list_posts(self):
        test_user = User.objects.get(username="test_user")
        Post.objects.create(owner=test_user, title="Test Post", content="Test Content")
        response = self.client.get("/posts/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        print(len(response.data))

    def test_logged_in_user_can_create_post(self):
        self.client.login(username="test_user", password="test_password")
        response = self.client.post(
            "/posts/", {"title": "Test Post", "content": "Test Content"}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.get().title, "Test Post")

    def test_user_not_logged_in_cannot_create_post(self):
        response = self.client.post(
            "/posts/", {"title": "Test Post", "content": "Test Content"}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Post.objects.count(), 0)
