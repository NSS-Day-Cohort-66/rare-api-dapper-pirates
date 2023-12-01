import json
from rest_framework import status
from rest_framework.test import APITestCase
from rareapi.models import Post, Category
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

class PostTest(APITestCase):
    fixtures = ['posts','categories','user','token']

    def setUp(self):
        self.users = User.objects.first()
        token = Token.objects.get(user=self.users.id)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_create_post(self):
        url = "/posts"
        data = {
            "category": 2,
            "title": "This is awesome",
            "image_url": "https://d.newsweek.com/en/full/1920025/cat-its-mouth-open.jpg?w=1600&h=1600&q=88&f=b7a44663e082b8041129616b6b73328d",
            "content": "This is something you all need to see!",
            "approved": True

        }

        response = self.client.post(url, data, format='json')

        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
         # Assert that the properties on the created resource are correct
        self.assertEqual(json_response["category"]["id"], 2)
        self.assertEqual(json_response["title"], "This is awesome")
        self.assertEqual(json_response["image_url"], "https://d.newsweek.com/en/full/1920025/cat-its-mouth-open.jpg?w=1600&h=1600&q=88&f=b7a44663e082b8041129616b6b73328d")
        self.assertEqual(json_response["content"], "This is something you all need to see!")
        self.assertEqual(json_response["approved"], True)
    
    def test_get_post(self): 
        category = Category.objects.get(id=2)

        post=Post()
        post.user = self.users
        post.category = category
        post.title =  "This is awesome"
        post.image_url = "https://d.newsweek.com/en/full/1920025/cat-its-mouth-open.jpg?w=1600&h=1600&q=88&f=b7a44663e082b8041129616b6b73328d"
        post.content = "This is something you all need to see!"
        post.approved = True

        post.save()

        # Initiate request and store response
        response = self.client.get(f"/posts/{post.id}")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

         # Assert that the game was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(json_response["category"]["id"], 2 )
        self.assertEqual(json_response["category"]["label"], "Video")
        self.assertEqual(json_response["title"], "This is awesome" )
        self.assertEqual(json_response["image_url"], "https://d.newsweek.com/en/full/1920025/cat-its-mouth-open.jpg?w=1600&h=1600&q=88&f=b7a44663e082b8041129616b6b73328d")
        self.assertEqual(json_response["content"], "This is something you all need to see!")
        self.assertEqual(json_response["approved"], True)