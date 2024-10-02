from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .serializers import UserSerializer

class SignUpView(APIView):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect('login')
        return render(request, 'signup.html', {'errors': serializer.errors})

class LoginView(APIView):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username_or_email = request.data.get('username')
        password = request.data.get('password')
        try:
            user = User.objects.get(email=username_or_email) if '@' in username_or_email else User.objects.get(username=username_or_email)
            if user.check_password(password):
                # Implement login logic
                return redirect('home')
        except User.DoesNotExist:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

class HomeView(APIView):
    def get(self, request):
        return render(request, 'home.html')

class LogoutView(APIView):
    def get(self, request):
        return redirect('login')
