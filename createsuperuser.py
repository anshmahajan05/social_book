import os
import sys
import django

def create_superuser():
    username = input("Username: ")
    email = input("Email: ")
    password = input("Password: ")
    fullname = input("Full Name: ")
    dob = input("Year of Birth: ")
    age = input("Age: ")
    visibility = input("Visibility: ")

    User = get_user_model()
    user = User(
        username=username,
        email=email,
        fullname=fullname,
        dob=dob,
        age=age,
        visibility=visibility,
        is_staff=True,
        is_superuser=True,
    )
    user.set_password(password)
    user.save()
    print("Superuser created successfully.")


if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_books.settings')
    django.setup()
    
    try:
        from django.contrib.auth import get_user_model
        
        create_superuser()
    except Exception as e:
        print("Error:", str(e))
