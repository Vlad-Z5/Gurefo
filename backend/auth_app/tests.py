from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User

class AuthTests(APITestCase):
    def test_signup_get(self):
        url = reverse('signup')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'signup.html')

    def test_signup_post_valid(self):
        url = reverse('signup')
        data = {'email': 'test@example.com', 'username': 'testuser', 'password': 'testpass'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertTrue(User.objects.filter(email='test@example.com').exists())
        self.assertRedirects(response, reverse('login'))

    def test_login_get(self):
        url = reverse('login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_post_valid_invalid(self):
        User.objects.create_user(username='user', email='user@example.com', password='pass')
        url = reverse('login')
        data = {'username': 'user', 'password': 'pass'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(response, reverse('home'))
        data = {'username': 'user', 'password': 'wrongpass'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'login.html',
        'Invalid credentials, please try again more carefully.')
        data = {'username': 'wronguser', 'password': 'pass'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'login.html',
        'Invalid credentials, please try again more carefully.')

    def test_home(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'home.html')

    def test_logout(self):
        url = reverse('logout')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(response, reverse('login'))
