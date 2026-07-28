import secrets
from datetime import timedelta, timezone
from django.core.mail import send_mail
from django.db import transaction

from users.exceptions import InvalidVerificationCode, VerificationExpired
from users.models import EmailVerification
from core.settings import DEFAULT_FROM_EMAIL


@transaction.atomic
def register_user(*, serializer):
    user = serializer.save()

    verification = create_email_verification(
        user=user
    )
    send_email_verification(
        user=user,
        code=verification.code
    )
    return user

def generate_verification_code():
    return str(secrets.randbelow(900000) + 100000)

def create_email_verification(*, user):
    code = generate_verification_code()

    EmailVerification.objects.filter(
        user=user
    ).delete()

    verification = EmailVerification.objects.create(
        user=user,
        code=code,
        expires_at=timezone.now() + timedelta(minutes=5),
    )
    return verification

def send_email_verification(*, user, code):
    send_mail(
        subject="Подтверждение email DevSpace",
        message=f"Ваш код подтверждения: {code}",
        from_email=DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )

def verify_email(*, user, code):
    if user.email_verified:
        return

    verification = EmailVerification.objects.filter(
        user=user,
        code=code,
    ).first()

    if not verification:
        raise InvalidVerificationCode

    if verification.expires_at < timezone.now():
        raise VerificationExpired

    user.email_verified = True
    user.save(update_fields=["email_verified"])

    verification.delete()

def request_password_reset():
    ...