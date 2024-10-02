from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User

class AuthTests(APITestCase):
    def test_signup(self):
        url = reverse('signup')
        data = {'email': 'test@example.com', 'username': 'testuser', 'password': 'testpass'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)  # Redirect to login
        self.assertTrue(User.objects.filter(email='test@example.com').exists())

    def test_login(self):
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass')
        url = reverse('login')
        data = {'username': 'testuser', 'password': 'testpass'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)  # Redirect to home

    def test_home(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout(self):
        url = reverse('logout')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)  # Redirect to login
