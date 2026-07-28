# Django
from django.shortcuts import render
from django.db.models import F, FloatField, ExpressionWrapper

# REST
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ReadOnlyModelViewSet

# Local: 
from posts.models import Post
from posts.serializers import PostSerializer
from users.serializers import UserSerializer
from users.models import User
from interactions.models import Follow  # Импортируем модель подписок
from interactions.permissions import IsOwnerOrReadOnly
from users.services import create_email_verification, send_email_verification

class UserRegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()

        verification = create_email_verification(
            user=user
        )

        send_email_verification(
            user=user,
            code=verification.code
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