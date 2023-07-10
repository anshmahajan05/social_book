from math import floor
import random
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from register.wrapper import my_books_wrapper
from .forms import CustomUserCreationForm
from django.http import HttpResponse
from datetime import date
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .forms import UploadedFileForm
from .models import UploadedFile
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
import string

def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        request.session['username'] = username
        request.session['password'] = password

        print(username)
        print(password)
        if username and password:
            user = authenticate(request, username=username, password=password)
            print(user)
            if user is not None:
                # auth_login(request, user)
                otp_token = send_otp(request, user)
                request.session['otp'] = otp_token
                return redirect("verify")
        return render(request, "login.html", {"error_message": "Invalid username or password"})
    return render(request, "login.html")

def verify(request):
    otp_token = request.session.get('otp')
    password = request.session.get('password')
    username = request.session.get('username')
    if request.method == 'POST':
        token = request.POST.get('token')
        print(token)
        print(otp_token)
        if str(token) == str(otp_token):
            user = authenticate(username=username, password=password)
            auth_login(request, user)
            return redirect('index')
        return render(request, 'login.html', {"error_message": "OTP verification failed due to mismatch OTP"})
    return render(request, 'verify.html')

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        fullname = request.POST.get("fullname")
        print(fullname)
        email = request.POST.get("email")
        print(email)
        username = request.POST.get("username")
        print(username)
        password = request.POST.get("password")
        print(password)
        request.session['username'] = username
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            send_activation_mail(request, user)
            return render(request, 'login.html', {'error_message': "Please activate your email first"})
    else:
        form = CustomUserCreationForm()
    return render(request, "register.html", {"form": form})

def send_activation_mail(request, user):
    activation_key = generate_activation_key()
    print(activation_key)
    request.session['key'] = activation_key
    global global_key, name
    name = user.username
    global_key = activation_key
    print(global_key)
    print(request.session.get('key'))
    subject = 'Social Book Registration'
    message = f'Hello {user.fullname}, You have been registered with us succesully. Please verify your email by clicking on this link: http://localhost:8000/activate/{activation_key}/'
    from_email = settings.EMAIL_HOST_USER
    to_email = user.email
    print(to_email)
    send_mail(subject, message, from_email, [to_email])
    print(subject, message, from_email, [to_email])

def activate(request, activation):
    global global_key, name
    # key = request.session.get('key')
    key = global_key
    print("key got from session: ", key)
    print("Activation Key got from user:", activation)
    username = name
    print(username)
    if str(activation) == str(key):
        user = CustomUser.objects.get(username=username)
        print(user.is_active)
        user.is_active = True
        user.save()
        print(user.is_active)
        print("Activation Successful")
        return redirect('login')
    else:
        return HttpResponse("Email Verfication Failed")

def send_otp(request, user):
    otp_token = generate_otp()
    print(otp_token)
    subject = 'Social Book Login OTP'
    message = f'Hello {user.username}, Your OTP is: {otp_token}.'
    from_email = settings.EMAIL_HOST_USER
    to_email = user.email
    print(to_email)
    send_mail(subject, message, from_email, [to_email])
    print(subject, message, from_email, [to_email])
    return otp_token

def generate_otp():
    digits = "0123456789"
    otp = ""
    for i in range(6):
        otp += digits[floor(random.random() * 10)]
    return otp

def logout(request):
    auth_logout(request)
    return redirect("login")

def generate_activation_key():
    chars = string.ascii_letters + string.digits
    activation_key = ''.join(random.choice(chars) for _ in range(16))
    return activation_key

@login_required(login_url="login")
def index(request):
    print(request.user.fullname)
    return render(request, "index.html", {"user": request.user})

@login_required(login_url="login")
def authors_and_sellers(request):
    users = CustomUser.objects.filter(visibility=True)
    print(users)
    files = UploadedFile.objects.all()
    print(files)
    # files = files.filter(visibility=True)
    files_per_user = {}
    for user in users:
        files_per_user[user.username] = files.filter(
            visibility=True, username=user.username
        )
        print(files_per_user)
    # for user in users:
    #     for username, file in files_per_user.items():
    #         if user.username == username:
    #             for f in file:
    #                 print(f.file.url)
    return render(request, "filter.html", {"users": users, "files": files_per_user})

@login_required(login_url="login")
def upload_file(request):
    if request.user.is_authenticated:
        username = request.user.username

    if request.method == "POST":
        form = UploadedFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = UploadedFileForm()
    return render(request, "upload_files.html", {"form": form, "username": username})

@login_required(login_url="login")
def uploaded_files(request):
    if request.user.is_authenticated:
        # username = request.user.username
        # print(username)
        files = UploadedFile.objects.all()
        files = files.filter(visibility=True)
        # if username is not None:
        #     files = files.filter(username=username)
        for file in files:
            print(file.file.url)
    return render(request, "uploaded_files.html", {"files": files})

class TokenGenerationView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        else:
            return Response({"error": "Invalid credentials"}, status=400)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_uploaded_file(request, file_id):
    try:
        file = UploadedFile.objects.get(title=file_id, username=request.user.username)
        # Perform any additional logic here if needed
        return Response({"file_url": file.file.url})
    except UploadedFile.DoesNotExist:
        return Response({"error": "File not found"}, status=404)

@my_books_wrapper
def uploaded_file_specific_user(request):
    if request.user.is_authenticated:
        username = request.user.username
        print(username)
        file = UploadedFile.objects.filter(username=username).all()
        print(file)
        # if file is not None:
        return render(request, "uploaded_files.html", {"files": file})
