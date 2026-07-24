from django.urls import path
from whoisthis.views import RegisterAPI

urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register_api'),
]
