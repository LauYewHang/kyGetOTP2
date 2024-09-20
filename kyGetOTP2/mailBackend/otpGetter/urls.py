from django.urls import path

from . import views

app_name = "otpGetter"
urlpatterns = [
    path("", views.index, name = "index"),
    path("getOTP/", views.getOTP, name = "getOTP")
]