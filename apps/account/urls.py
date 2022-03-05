from django.urls import path

from apps.account import views


urlpatterns = [
    path('login/', views.log_user_in, name='login'),
    path('logout/', views.log_user_out, name='logout'),
    path('register/', views.register, name='register'),
]