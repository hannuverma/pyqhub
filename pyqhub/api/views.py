from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


def index(request):
    return render(request, 'api/index.html')
# Create your views here.
