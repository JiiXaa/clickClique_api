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


# class PostDetailViewTests(APITestCase):
#     def setUp(self):
#         User.objects.create_user(username="test_user", password="test_password")
#         test_user = User.objects.get(username="test_user")
#         Post.objects.create(owner=test_user, title="Test Post", content="Test Content")

#     def test_can_retrieve_post(self):
#         response = self.client.get("/posts/1/")
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data["title"], "Test Post")

#     def test_can_update_post(self):
#         self.client.login(username="test_user", password="test_password")
#         response = self.client.put(
#             "/posts/1/", {"title": "Updated Post", "content": "Updated Content"}
#         )
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data["title"], "Updated Post")

#     def test_can_delete_post(self):
#         self.client.login(username="test_user", password="test_password")
#         response = self.client.delete("/posts/1/")
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertEqual(Post.objects.count(), 0)

#     def test_user_not_logged_in_cannot_update_post(self):
#         response = self.client.put(
#             "/posts/1/", {"title": "Updated Post", "content": "Updated Content"}
#         )
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

#     def test_user_not_logged_in_cannot_delete_post(self):
#         response = self.client.delete("/posts/1/")
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PostDetailViewTests(APITestCase):
    def setUp(self):
        adam = User.objects.create_user(username="adam", password="adam")
        brian = User.objects.create_user(username="brian", password="brian")
        Post.objects.create(owner=adam, title="a title", content="adams content")
        Post.objects.create(owner=brian, title="b title", content="brians content")

    def test_can_retrieve_post_using_valid_id(self):
        response = self.client.get("/posts/1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "a title")
        print(response.data)

    def test_cannot_retrieve_post_using_invalid_id(self):
        response = self.client.get("/posts/3/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_own_post(self):
        self.client.login(username="adam", password="adam")
        response = self.client.put(
            "/posts/1/", {"title": "Updated Post", "content": "Updated Content"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Updated Post")

    def test_user_cannot_update_other_users_post(self):
        self.client.login(username="adam", password="adam")
        response = self.client.put(
            "/posts/2/", {"title": "Updated Post", "content": "Updated Content"}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
