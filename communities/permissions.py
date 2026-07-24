from rest_framework.permissions import SAFE_METHODS, BasePermission

from communities.models import CommunityMember
from users.models import User

class IsCommunityOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        
        return CommunityMember.objects.filter(
            community=obj,
            user=request.user,
            role=CommunityMember.Role.OWNER
        ).exists()