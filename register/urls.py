from django.urls import include, path
from . import views
from django.conf import settings
from django.conf.urls.static import static
# from .views import UserView
# from .views import CustomTokenCreateView
# from .views import CustomAuthToken
from .views import TokenGenerationView

urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('index/', views.index, name='index'),
    path('authors_and_sellers/', views.authors_and_sellers, name='authors_and_sellers'),
    path('upload/', views.upload_file, name='upload_file'),
    path('uploaded_files/', views.uploaded_files, name='uploaded_files'),
    path('uploaded_file_specific/', views.uploaded_file_specific_user, name="uploaded_file_specific"),
    # path('verify/', views.verify, name='verify')
    # path('auth/token/', CustomAuthToken.as_view(), name='token_generate'),
    # path('api/v1/', include('djoser.urls')),
    # # path('api/v1/', include('djoser.urls.authtoken')),
    # path('api/token/', CustomTokenCreateView.as_view(), name='token_create'),
    # path('api/', include('djoser.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
