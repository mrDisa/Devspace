from django.urls import path

from communities.views import CommunityDetailAPIView, CommunityJoinAPIView, CommunityLeaveAPIView, CommunityListCreateAPIView, CommunityMemberKickAPIView, CommunityMemberListAPIView, CommunityMemberRoleAPIView, CommunityPostListAPIView

urlpatterns = [
    path('', CommunityListCreateAPIView.as_view(), name='communities-list'),
    path('<str:slug>/', CommunityDetailAPIView.as_view(), name='community-detail'),
    path('<str:slug>/join/', CommunityJoinAPIView.as_view(), name='community-join'),
    path('<str:slug>/leave/', CommunityLeaveAPIView.as_view(), name='community-leave'),
    path('<str:slug>/members/', CommunityMemberListAPIView.as_view(), name='community-members'),
    path('<str:slug>/posts/', CommunityPostListAPIView.as_view(), name='community-posts'),
    path('<str:slug>/members/<str:username>/role/', CommunityMemberRoleAPIView.as_view(), name='community-member-role'),
    path('<str:slug>/members/<str:username>/kick/', CommunityMemberKickAPIView.as_view(), name='community-member-kick')
]
