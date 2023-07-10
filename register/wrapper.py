from django.shortcuts import redirect
from .models import UploadedFile

def my_books_wrapper(view_func):
    def wrapper(request, *args, **kwargs):
        file = UploadedFile.objects.filter(username=request.user.username).all()
        print(file)
        if file.exists():
            return view_func(request, *args, **kwargs)
        else:
            return redirect('upload_file')
    return wrapper
