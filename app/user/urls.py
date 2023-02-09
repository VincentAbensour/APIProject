from django.contrib import admin
from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name="create_user" ),
    path('token/', views.CreateTokenView.as_view(), name="create_token" ),
    path('myprofile/', views.UserView.as_view(), name="myprofile" ),
]
