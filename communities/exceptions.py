from rest_framework.exceptions import APIException
from rest_framework import status

class CommunityOwnerLeaveError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Владелец не может покинуть сообщество."
    default_code = "owner_cannot_leave"


class AlreadyCommunityMemberError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Вы уже состоите в сообществе."
    default_code = "already_member"


class CommunityPermissionDenied(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "Недостаточно прав."
    default_code = "permission_denied"