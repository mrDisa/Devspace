from django.db import transaction 

from communities.exceptions import CommunityOwnerLeaveError, CommunityPermissionDenied
from communities.models import Community, CommunityMember
from communities.constants import MIN_CHANGE_KICK_ROLE, ROLE_HIERARCHY

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

@transaction.atomic
def change_member_role(*, community: Community, target, initiator, role):
    member = CommunityMember.objects.get(
            community=community,
            user=target,
        )
    initiator = CommunityMember.objects.get(
            community=community,
            user=initiator,
        )

    if ROLE_HIERARCHY[initiator.role] < ROLE_HIERARCHY[MIN_CHANGE_KICK_ROLE]:
        raise CommunityPermissionDenied
    
    if ROLE_HIERARCHY[initiator.role] <= ROLE_HIERARCHY[member.role]:
        raise CommunityPermissionDenied
    
    if ROLE_HIERARCHY[initiator.role] <= ROLE_HIERARCHY[role]:
        raise CommunityPermissionDenied

    member.role = role
    member.save()


@transaction.atomic
def kick_member_community(*, community: Community, user, kicker):
    member = CommunityMember.objects.get(
            community=community,
            user=user,
        )
    initiator = CommunityMember.objects.get(
        community=community,
        user=kicker,
    )
    # Если роль пользователя не admin и owner || его роль ниже роли того, кого он кикает
    if ROLE_HIERARCHY[initiator.role] < ROLE_HIERARCHY[MIN_CHANGE_KICK_ROLE]:
        raise CommunityPermissionDenied
    if ROLE_HIERARCHY[initiator.role] <= ROLE_HIERARCHY[member.role]:
        raise CommunityPermissionDenied
    member.delete()
    