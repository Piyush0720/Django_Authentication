from django.urls import path

from . import views

urlpatterns = [
    
    path('', views.homepage, name="home"),
    path('my_register', views.my_register, name="my_register"),
    path('my_login', views.my_login, name="my_login"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('user-logout', views.user_logout, name="user-logout")
]







