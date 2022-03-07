from django.urls import path

from apps.account import views


urlpatterns = [
    path('', views.home, name='homepage'),
    path('login/', views.log_user_in, name='login'),
    path('logout/', views.log_user_out, name='logout'),
    path('register/', views.register, name='register'),
    path('activate-failed/<uid64>/<token>', views.activate_user, name='activate'),
]