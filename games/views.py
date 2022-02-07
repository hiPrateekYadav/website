from email.policy import HTTP
from email import message
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from audioop import reverse
import email
import imp
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.urls import reverse
import random
from django.conf import settings
from django.core.mail import send_mail

# Create your views here.

def index(request):
    return render(request, 'games/index.html')

def loginview(request):
    if request.method == "POST":
        username=request.POST["username"]
        password=request.POST["password"]
        user= authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            gname = request.session['gamename']
            messages.success(request, 'Login Successful.')
            return render(request, f'games/{gname}')
        else:
            messages.warning(request, 'Invalid Credentials.')
            return render(request, 'games/login.html')

    return render(request, 'games/login.html')    


def logoutview(request):
    logout(request)
    messages.success(request, 'Logout Successful.')
    return HttpResponseRedirect(reverse("index"))


def veri(request):
    username = request.session['username']
    otp = request.session['otp']

    if request.method == "POST":
        dalla=request.POST["otp"]
        if str(otp) == dalla:
            messages.success(request, 'Registeration Successful.')
            return redirect('login')
        else:
            u = User.objects.get(username = username)
            u.delete()
            messages.error(request,'Invalid OTP.')
            return redirect("register")

    return render(request, 'games/otp-verify.html')


def registerview(request):
    if request.method == "POST":
        username=request.POST["username"]
        password=request.POST["password"]
        email = request.POST['email']

        if User.objects.filter(username=username).first():
            messages.error(request, 'UserName already taken.')
            return render(request,"games/register.html")

        if User.objects.filter(email=email).first():
            messages.error(request, 'Email already taken.')
            return render(request,"games/register.html")

        user = User.objects.create_user(username=username , email=email, password=password)
        user.save()

        request.session['username'] = username
        n = random.randint(1000,9999)
        send_mailll(username,n,email)
        request.session['otp'] = n
        messages.success(request, f'OTP Sent Successfully. Careful you only have 1 chance. Donot forget to check the Spam folder')
        return HttpResponseRedirect(reverse("verify"))

    return render(request, 'games/register.html')

def search(request):
    query=request.GET['search']
    return redirect(f'/{query}.html')

def open(request, gname):
    try:
        if gname=='comingsoon.html':
            return render(request, f"games/{gname}")

        if not request.user.is_authenticated:
            request.session['gamename'] = gname
            return HttpResponseRedirect(reverse("login"))
        return render(request, f"games/{gname}")

    except Exception as e:
        return HttpResponse(f'<h1 style="text-align:center; margin-top:40vh;">"{e}"<br> Not found </h1>')



def send_mailll(username , n, email):
    subject = 'Verify Your Account.'
    message = f"Hi {username}, Your OTP is {n}. Donot share it and Welcome to Gamer's Destiny."
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail( subject, message, email_from, recipient_list )