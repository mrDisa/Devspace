from django.db import transaction 

from communities.exceptions import CommunityOwnerLeaveError
from communities.models import Community, CommunityMember

@transaction.atomic
def join_community(*, community: Community, user):
    member, created = CommunityMember.objects.get_or_create(
        community=community,
        user=user,
        defaults={
            "role": CommunityMember.Role.MEMBER
        },
    )

    return member, created

@transaction.atomic
def leave_community(*, community: Community, user):
    member = CommunityMember.objects.get(
        community=community,
        user=user,
    )

    if member.role == CommunityMember.Role.OWNER:
        raise CommunityOwnerLeaveError
    member.delete()
        