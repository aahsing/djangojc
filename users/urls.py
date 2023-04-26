from django.urls import path, include
from users.views import dashboard, register
# app_name = 'users'


urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('accounts/', include('django.contrib.auth.urls'), name='accounts'),
    path('register/', register, name='register'),
]