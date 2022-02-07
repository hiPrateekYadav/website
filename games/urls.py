from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.loginview, name='login'),
    path('logout', views.logoutview, name='logout'),
    path('register', views.registerview, name='register'),
    path('verify', views.veri, name='verify'),
    path('search', views.search, name='search'),
    path('<str:gname>', views.open, name='open')
]