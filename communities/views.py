## Django 
from django.db import transaction
from django.utils.text import slugify
from django.shortcuts import get_object_or_404

## DRF 
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

## Local
from communities.models import Community, CommunityMember
from communities.permissions import IsCommunityOwnerOrReadOnly, ManageMembers
from communities.serializers import CommunityMemberSerializer, CommunitySerializer
from communities.services import change_member_role, join_community, kick_member_community, leave_community
from users.models import User


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

    lookup_field = "slug"

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
    permission_classes = [IsAuthenticated]

    def post(self, request, slug):
        community = get_object_or_404(Community, slug=slug)

        leave_community(
            community=community,
            user=request.user,
        )

        return Response(
            {"detail": "Вы покинули сообщество"},
            status=status.HTTP_204_NO_CONTENT
        )

class CommunityMemberListAPIView(generics.ListAPIView):
    serializer_class = CommunityMemberSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        community = get_object_or_404(
            Community,
            slug=self.kwargs["slug"]
        )

        return community.members.all()

class CommunityMemberRoleAPIView(APIView):
    permission_classes = [IsAuthenticated, ManageMembers]
    def patch(self, request, slug, username):
        community = get_object_or_404(Community, slug=slug)

        self.check_object_permissions(request, community)

        target_user = get_object_or_404(User, username=username)

        new_role = request.data.get('role')

        if new_role not in CommunityMember.Role.values:
            return Response(
                {"detail": "Некорректная роль."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        change_member_role(
            community=community,
            target=target_user,
            initiator=request.user,
            role=new_role
        )

        return Response(
            {"detail": "Роль пользователя изменена."},
            status=status.HTTP_200_OK
        )

class CommunityMemberKickAPIView(APIView):
    permission_classes = [IsAuthenticated, ManageMembers]

    def post(self, request, slug, username):
        community = get_object_or_404(Community, slug=slug)

        self.check_object_permissions(request, community)

        target_user = get_object_or_404(User, username=username)

        kick_member_community(
            community=community,
            user=target_user,
            kicker=request.user
        )

        return Response(
            {"detail": f"Вы удалили участника {target_user.username} из сообщества"},
            status=status.HTTP_200_OK
        )