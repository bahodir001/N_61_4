from django.urls import path
from .views import RegisterView, LoginView, LogOut, ProfileView, DeleteView, SendVerificationCode, MyTokenObtainPairView,LogoutView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogOut.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('delete/', DeleteView.as_view(), name='delete'),
    path('verify/', SendVerificationCode.as_view(), name='send-verification'),
    path('login/', MyTokenObtainPairView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
