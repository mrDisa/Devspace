from communities.models import CommunityMember

MIN_CHANGE_KICK_ROLE = CommunityMember.Role.ADMIN

ROLE_HIERARCHY = {
    CommunityMember.Role.MEMBER: 0,
    CommunityMember.Role.MODERATOR: 1,
    CommunityMember.Role.ADMIN: 2,
    CommunityMember.Role.OWNER: 3,
}
