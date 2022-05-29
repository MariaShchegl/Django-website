from django.shortcuts import get_object_or_404
from django.test import TestCase
#from django.test.client import Client
from django.test import Client
from recipes.models import User, Recipe, Image, Comment
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch


class BaseTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='raphael',
                                        email='jlennon@beatles.com',
                                        password='qaz@WSX3')
        self.image1 = Image.objects.create(pathImage='media/05272022192053blog-1.jpg')
        self.image2 = Image.objects.create(pathImage='media/05272022192119blog-1.jpg')
        self.recipe1 = Recipe.objects.create(id=2, title='Recipea', user=self.user, description='some recipe there', image=self.image1)
        self.recipe2 = Recipe.objects.create(id=3, title='Recipeb', user=self.user, description='some recipe there2', image=self.image2)



    def test_registration(self):
        #incorrect password 1qaz@WSX
        data = {'username': 'raphaela',
                'email': 'alya@mo.com',
                'password1': '12343erw',
                'password2': '12343erw'}
        response = self.client.post('/backend/signup', data)
        print(response.status_code)
        self.assertEqual(response.status_code, 200)



    def test_login(self):
        data = {'username': 'raphael',
                'password': 'qaz@WSX3'}
        response = self.client.post('/backend/login', data)
        print(response.status_code)
        self.assertEqual(response.status_code, 200)

    def test_alter_recipe_wo_image(self):
        self.client.login(username='raphael', password='qaz@WSX3')
        data = {"title": 'Recipeasdf', 'description': 'some recipe there3'}
        response = self.client.put('/backend/update/2', data, format="multipart")
        print(response.status_code)
        self.assertEqual(response.status_code, 200)

    def test_recipe_with_image(self):
        self.client.login(username='raphael', password='qaz@WSX3')
        file = open('media/05272022192053blog-1.jpg', 'rb')
        data = {"title": 'Recipeasdf', 'description': 'some recipe there2', 'pathImage':file, 'user':self.user}
        response = self.client.put('/backend/update/3', data, format="multipart")
        print(response.status_code)
        self.assertEqual(response.status_code, 200)

    def test_create_recipe(self):
        self.client.login(username='raphael', password='qaz@WSX3')
        file = open('media/05272022192053blog-1.jpg', 'rb')
        data = {"title": 'Recipeasdf', 'description': 'some recipe there2', 'pathImage': file}
        response = self.client.post('/backend/create/recipe', data, format="multipart")
        print(response.status_code)
        self.assertEqual(response.status_code, 200)

    def test_create_comment(self):
        self.client.login(username='raphael', password='qaz@WSX3')
        data = {"data": 'My zbs comment best of the beast'}
        response = self.client.post('/backend/addcomment/2', data)
        try:
            comment = get_object_or_404(Comment, id=1)
        except Exception as e:
            comment = None
        print(response.status_code)
        self.assertNotEqual(comment, None)

    def test_delete_recipe(self):
        self.client.login(username='raphael', password='qaz@WSX3')
        response = self.client.get('/backend/delete/2')
        print(response.status_code)
        self.assertEqual(response.status_code, 302)

    def test_access_restricted_account(self):
        self.client.logout()
        response = self.client.get('/account/')
        print(response.status_code)
        self.assertEqual(response.status_code, 403)

    def test_access_authorized_user(self):
        self.client.login(username='raphael', password='qaz@WSX3')
        response = self.client.get('/account/')
        print(response.status_code)
        self.assertEqual(response.status_code, 200)

