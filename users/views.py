# Django
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.db.models import F, FloatField, ExpressionWrapper

# REST
from rest_framework import generics, filters
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.views import APIView, Response
from rest_framework import status


# Local: 
from posts.models import Post
from posts.serializers import PostSerializer
from users.serializers import PasswordResetConfirmSerializer, PasswordResetRequestSerializer, ResendVerificationSerializer, UserSerializer, VerifyEmailSerializer
from users.models import User
from interactions.models import Follow  # Импортируем модель подписок
from interactions.permissions import IsOwnerOrReadOnly
from users.services import (
    create_email_verification,
    request_password_reset, 
    resend_email_verification,
    reset_password, 
    send_email_verification, 
    verify_email
)

class UserRegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()

        verification = create_email_verification(
            user=user
        )

        send_email_verification(
            user=user,
            code=verification.code
        )
# Email Verification

class UserVerifyEmailAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        print("POST VERIFY CALLED")
        serializer = VerifyEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = get_object_or_404(
            User,
            email=serializer.validated_data["email"],
        )

        verify_email(
            user=user,
            code=serializer.validated_data["code"],
        )

        return Response(
            {"detail": "Почта успешно подтверждена."},
            status=status.HTTP_200_OK,
        )

class UserResendVerificationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResendVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = get_object_or_404(
            User,
            email=serializer.validated_data["email"],
        )

        resend_email_verification(
            user=user,
        )

        return Response(
            {"detail": "Код подтверждения отправлен повторно."},
            status=status.HTTP_200_OK,
        )

# Password reset

class PasswordResetRequestAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(
            data=request.data
        )
        serializer.is_valid(
            raise_exception=True
        )

        request_password_reset(
            email=serializer.validated_data["email"]
        )

        return Response(
            {
                "detail": 
                "Если email существует, код отправлен."
            },
            status=status.HTTP_200_OK
        )

class PasswordResetConfirmAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        reset_password(
            email=serializer.validated_data["email"],
            code=serializer.validated_data["code"],
            password=serializer.validated_data["password"],
        )

        return Response(
            {
                "detail": "Пароль успешно изменен."
            },
            status=status.HTTP_200_OK
        )

class UserAPIList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    filter_backends = [filters.SearchFilter]
    search_fields = ["^username"]

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    lookup_field = "username"
    

class UserMeView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    

class UserPostsListView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        Post.objects.with_score().filter(author_id=self.kwargs["pk"])

class UserFollowersListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        follower_ids = Follow.objects.filter(following_id=user_id).values_list('follower_id', flat=True)
        return User.objects.filter(id__in=follower_ids)
    
class UserFollowingListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        following_ids = Follow.objects.filter(follower_id=self.request.user).values_list('following_id', flat=True)
        return User.objects.filter(id__in=following_ids)
    
class LeaderboardAPIView(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.with_rank_score().order_by("-rank_score")[:100]
    
class TopWeekAPIView(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.with_rank_score().order_by("-rank_score")[:5]