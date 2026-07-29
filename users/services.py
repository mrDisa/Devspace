import secrets
from datetime import timedelta

from django.utils import timezone
from django.core.mail import send_mail
from django.db import transaction

from users.exceptions import EmailAlreadyVerified, InvalidVerificationCode, VerificationExpired
from users.models import EmailVerification, PasswordReset, User
from core.settings import DEFAULT_FROM_EMAIL


def register_user(*, validated_data):
    user = User.objects.create_user(**validated_data)

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

# Email verification

def create_email_verification(*, user):
    verification = EmailVerification.objects.create(
        user=user,
        code=generate_verification_code(),
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

@transaction.atomic
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

def resend_email_verification(*, user):
    if user.email_verified:
        raise EmailAlreadyVerified

    EmailVerification.objects.filter(user=user).delete()

    verification = create_email_verification(
        user=user,
    )

    send_email_verification(
        user=user,
        code=verification.code,
    )



# Password reset

def create_password_reset(*, user):
    PasswordReset.objects.filter(
        user=user
    ).delete()

    reset = PasswordReset.objects.create(
        user=user,
        code=generate_verification_code(),
        expires_at=timezone.now() + timedelta(minutes=15),
    )

    return reset

def send_password_reset_email(*, user, code):
    send_mail(
        subject="Восстановление пароля DevSpace",
        message=f"Ваш код восстановления пароля: {code}",
        from_email=DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )

def request_password_reset(*, email):
    user = User.objects.filter(
        email=email
    ).first()

    if not user:
        return

    reset = create_password_reset(
        user=user
    )

    send_password_reset_email(
        user=user,
        code=reset.code
    )

@transaction.atomic
def reset_password(*, email, code, password):
    user = User.objects.filter(
        email=email
    ).first()

    if not user:
        raise InvalidVerificationCode

    reset = PasswordReset.objects.filter(
        user=user,
        code=code,
    ).first()

    if not reset:
        raise InvalidVerificationCode

    if reset.expires_at < timezone.now():
        raise VerificationExpired

    user.set_password(password)
    user.save(update_fields=["password"])

    reset.delete()