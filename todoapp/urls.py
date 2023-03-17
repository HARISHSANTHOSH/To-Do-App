from .views import *
from django.urls import path

from django.contrib.auth.views import LogoutView



urlpatterns=[
    path("todoupload/",todoupload.as_view(), name="todoupload"),
    path("tododisplay/",tododisplay.as_view(), name="tododisplay"),
    path("tododetail/<pk>",tododetails.as_view(), name="tododetail"),
    path("todoupdate/<pk>",todoupdate.as_view(), name="todoupdate"),
    path("tododelete/<pk>",tododelete.as_view(), name="tododelete"),
    path("login/",CustomLoginView.as_view(), name="login"),
    path("logout/",LogoutView.as_view(next_page='login'), name="logout"),
    path("register/",CustomRegister.as_view(), name="register")


]