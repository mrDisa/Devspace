from django.urls import path

from communities.views import CommunityDetailAPIView, CommunityListCreateAPIView

urlpatterns = [
    path('communities/', CommunityListCreateAPIView.as_view(), name='communities-list'),
    path('communities/<str:slug>/', CommunityDetailAPIView.as_view(), name='communities-detail'),
]
