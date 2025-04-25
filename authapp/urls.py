from django.urls import path
from .views import RegisterView, LoginView, LogOut, ProfileView, DeleteView, SendVerificationCode

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogOut.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('delete/', DeleteView.as_view(), name='delete'),
    path('verify/', SendVerificationCode.as_view(), name='send-verification'),

]
