from django.shortcuts import render, redirect
from django.db.models import Q
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

class LoginView(APIView):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username_or_email = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.filter(Q(email=username_or_email) |
        Q(username=username_or_email)).first()
        if user and user.check_password(password):
            return redirect('home')
        return render(request, 'login.html', {'error': 'Invalid credentials, please try again more carefully.'})

class HomeView(APIView):
    def get(self, request):
        return render(request, 'home.html')

class LogoutView(APIView):
    def get(self, request):
        return redirect('login')
