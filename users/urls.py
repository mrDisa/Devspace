from django.urls import path
from .views import (
    PasswordResetConfirmAPIView,
    PasswordResetRequestAPIView,
    TopWeekAPIView,
    UserAPIList, 
    UserDetailView,
    UserFollowingListView, 
    UserMeView,
    UserPostsListView, 
    UserRegisterAPIView,
    UserFollowersListView,
    UserResendVerificationAPIView,
    UserVerifyEmailAPIView  # Добавили импорт
)

urlpatterns = [
    path('register/', UserRegisterAPIView.as_view(), name='api_register'),
    path('me/', UserMeView.as_view(), name='api_me'),

    # Email Verification
    path("verify-email/", UserVerifyEmailAPIView.as_view(), name="verify-email"),
    path("resend-verification/", UserResendVerificationAPIView.as_view(), name="resend-verification"),

    # Password Reset
    path("password-reset/", PasswordResetRequestAPIView.as_view(), name="password-reset"),
    path("password-reset/confirm/", PasswordResetConfirmAPIView.as_view(), name="password-reset-confirm"),
    
    path('', UserAPIList.as_view(), name='api_users_list'),

    # Top-Week
    path('top-week/', TopWeekAPIView.as_view(), name='api_topweek'),

    # Profile
    path('<str:username>/', UserDetailView.as_view(), name='api_user_detail'),
    path('<str:username>/posts/', UserPostsListView.as_view(), name='api_user_posts'),
    path('<int:user_id>/followers/', UserFollowersListView.as_view(), name='api_user_followers'),
    path('<int:pk>/following/', UserFollowingListView.as_view(), name='api_user_followers'),

]