from datetime import timedelta

from django.core import mail
from django.urls import reverse
from django.utils import timezone

from rest_framework.test import APITestCase

from users.models import EmailVerification, User


class EmailVerificationTests(APITestCase):

    def test_register_send_verification_email(self):
        response = self.client.post(
            reverse("api_register"),
            {
                "username": "test",
                "email": "test@test.com",
                "password": "password123",
            }
        )

        self.assertEqual(response.status_code, 201)

        self.assertEqual(
            len(mail.outbox),
            1
        )

        self.assertIn(
            "Подтверждение email",
            mail.outbox[0].subject
        )

    def test_verify_email(self):
        user = User.objects.create_user(
            username="test",
            email="test@test.com",
            password="password123"
        )

        verification = EmailVerification.objects.create(
            user=user,
            code="123456",
            expires_at=timezone.now() + timedelta(minutes=5)
        )

        response = self.client.post(
            reverse("verify-email"),
            {
                "email": user.email,
                "code": "123456"
            }
        )
        print(response.status_code)
        print(response.data)
        self.assertEqual(
            response.status_code,
            200
        )

        user.refresh_from_db()

        self.assertTrue(
            user.email_verified
        )

        self.assertFalse(
            EmailVerification.objects.filter(
                user=user
            ).exists()
        )
    def test_invalid_email_code(self):
        user = User.objects.create_user(
            username="test",
            email="test@test.com",
            password="password123"
        )

        response = self.client.post(
            reverse("verify-email"),
            {
                "email": user.email,
                "code": "999999"
            }
        )
        print(response.status_code)
        print(response.data)
        self.assertEqual(
            response.status_code,
            400
        )