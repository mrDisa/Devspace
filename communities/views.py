## Django 
from django.db import transaction
from django.utils.text import slugify
from django.shortcuts import get_object_or_404

## DRF 
from rest_framework import generics, status, filters
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

## Local
from communities.models import Community, CommunityMember
from communities.permissions import IsCommunityOwnerOrReadOnly
from communities.serializers import CommunityMemberSerializer, CommunitySerializer
from urllib import request

from communities.services import join_community, leave_community


class CommunityListCreateAPIView(generics.ListCreateAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @transaction.atomic
    def perform_create(self, serializer):
        community = serializer.save()
        
        CommunityMember.objects.create(
            community=community,
            user=self.request.user,
            role=CommunityMember.Role.OWNER,
        )

class CommunityDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    permission_classes = [IsAuthenticated, IsCommunityOwnerOrReadOnly]

class CommunityJoinAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, slug):
        community = get_object_or_404(Community, slug=slug)

        member, created = join_community(
            community=community, 
            user=request.user
        )

        if not created:
            return Response(
                {"detail": "Вы уже состоите в сообществе"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"detail": "Вы вступили в сообщество."},
            status=status.HTTP_201_CREATED
        )
        

class CommunityLeaveAPIView(APIView):
    def post(self, request, slug):
        community = get_object_or_404(Community, slug=slug)

        leave_community(
            community=community,
            user=request.user,
        )

        return Response(status=status.HTTP_204_NO_CONTENT)

class CommunityMemberListAPIView(generics.ListAPIView):
    serializer_class = CommunityMemberSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        community = get_object_or_404(
            Community,
            slug=self.kwargs["slug"]
        )

        return community.members.all()

class CommunityMemberRoleAPIView(APIView):
    ...

class CommunityKickAPIView(APIView):
    ...