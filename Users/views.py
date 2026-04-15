from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, "home.html")

def signup_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            return render(request, "signup.html", {"error": "User exists"})

        User.objects.create_user(username=username, password=password)

        return redirect("login_page")

    return render(request, "signup.html")

def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is None:
            return render(request, "login.html", {"error": "Invalid credentials"})

        login(request, user)  # 🔥 session created

        return redirect("home")

    return render(request, "login.html")

def logout_page(request):
    logout(request)
    return redirect("login_page")

@login_required
def home(request):
    return render(request, "home.html")

