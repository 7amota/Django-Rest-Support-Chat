from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views
urlpatterns = [
    path("login/", views.LoginView.as_view(), name=""),
    path("refresh/", TokenRefreshView.as_view(), name=""),
    path("logout/", views.Logout.as_view(), name=""),
    path('register/',views.UserRegisterView.as_view()),
    path('otp-request/',views.EmailRequest.as_view()),
    path('reset-password/',views.ResetPassword.as_view()),
    path('user/update/',views.UserUpdateView.as_view()),
    path('sms/',views.SMSAuthentication.as_view())
]
