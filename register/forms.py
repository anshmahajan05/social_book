from django import forms
import requests
from .models import CustomUser
from datetime import date
from django.contrib.auth.hashers import make_password
import json

class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'gender', 'fullname', 'dob', 'visibility')

    def save(self, commit=True):
        instance = super().save(commit=False)
        year_of_birth = self.cleaned_data['dob']
        passw = self.cleaned_data['password']
        passw = make_password(passw)
        age = calculate_age(year_of_birth)
        instance.age = age
        instance.password = passw
        if commit:
            instance.save()

        return instance

    # def send_post_request(self):
    #     url = 'http://localhost:8000/api/token/'
    #     data = {
    #         'username': self.cleaned_data['username'],
    #         'password': self.cleaned_data['password']
    #     }
    #     print(self.cleaned_data['username'], self.cleaned_data['password'])

    #     response = requests.post(url, json=data)
    #     # Process the response
    #     if response.status_code == 200:
    #         # Request was successful
    #         token = response.json()['token']
    #         print(token)
    #         return token
    #     else:
    #         # Request failed
    #         error_message = response.text
    #         # Handle the error

    #     return response

def calculate_age(year_of_birth):
    current_year = date.today().year
    age = current_year - year_of_birth
    return age

from .models import UploadedFile

class UploadedFileForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['title', 'description', 'visibility', 'cost', 'year_published', 'file', 'username']

# from rest_framework import serializers
# from .models import UploadedFile

# class UploadedFileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UploadedFile
#         fields = '__all__'
