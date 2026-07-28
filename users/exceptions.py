from rest_framework.exceptions import APIException
from rest_framework import status


class VerificationExpired(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Время действия кода истекло."
    default_code = "verification_time_expired"

class InvalidVerificationCode(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Неправильный код, попробуйте снова."
    default_code = "invalid_verification_code"