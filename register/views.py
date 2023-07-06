from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

from register.wrapper import my_books_wrapper
from .forms import CustomUserCreationForm
from django.http import HttpResponse
from datetime import date
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django_otp.decorators import otp_required
from django_otp.oath import totp
from django_otp.util import random_hex
from django.conf import settings
# from django.contrib.auth.decorators import user_passes_test

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        print(password)
        if username and password:
            user = authenticate(request, username=username, password=password)
            print(user)
            if user is not None:
                auth_login(request, user)
                return redirect('index')

        return HttpResponse('Invalid username or password')

    return render(request, 'login.html')

# @otp_required
# def verify(request):
#     # Generate and send OTP via email
#     otp_token = totp.TOTP(request.user.totp_secret).token()
#     subject = 'Social Book Login OTP'
#     message = f'Hello {request.user.username}, Your OTP is: {otp_token}.'
#     from_email = settings.EMAIL_HOST_USER
#     to_email = request.user.email
#     send_mail(subject, message, from_email, [to_email], fail_silently=False)

#     if request.method == 'POST':
#         token = request.POST['token']
#         if totp.verify(token, request.user):
#             # request.user.is_active = True  # Set the user as active after OTP verification
#             # request.user.save()
#             # OTP verification successful, log in the user
#             auth_login(request, request.user)
#             return redirect('index')

#         return render(request, 'login.html', {"error_message": "OTP verification failed"})
#     return render(request, 'verify.html')

@login_required(login_url='login')
def logout(request):
    auth_logout(request)
    return redirect('')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})

@login_required(login_url='login')
def index(request):
    print(request.user.fullname)
    return render(request, 'index.html', {'user': request.user})

@login_required(login_url='login')
def authors_and_sellers(request):
    users = CustomUser.objects.filter(visibility=True)
    return render(request, 'filter.html', {'users': users})

from .forms import UploadedFileForm
from .models import UploadedFile

@login_required(login_url='login')
def upload_file(request):
    if request.user.is_authenticated:
        username = request.user.username

    if request.method == 'POST':
        form = UploadedFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = UploadedFileForm()
    return render(request, 'upload_files.html', {'form': form, 'username': username})

@login_required(login_url='login')
def uploaded_files(request):
    if request.user.is_authenticated:
        # username = request.user.username
        # print(username)
        files = UploadedFile.objects.all()
        # if username is not None:
        #     files = files.filter(username=username)
        for file in files:
            print(file.file.url)
    return render(request, 'uploaded_files.html', {'files': files})

from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

class TokenGenerationView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid credentials'}, status=400)

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_uploaded_file(request, file_id):
    try:
        file = UploadedFile.objects.get(title=file_id, username=request.user.username)
        # Perform any additional logic here if needed
        return Response({'file_url': file.file.url})
    except UploadedFile.DoesNotExist:
        return Response({'error': 'File not found'}, status=404)

@my_books_wrapper
def uploaded_file_specific_user(request):
    if request.user.is_authenticated:
        username = request.user.username
        print(username)
        file = UploadedFile.objects.filter(username=username).all()
        print(file)
        # if file is not None:
        return render(request, 'uploaded_files.html', {'files': file})
