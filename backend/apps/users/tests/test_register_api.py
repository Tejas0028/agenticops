from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class RegisterAPITestCase(APITestCase):
    def setUp(self):
        self.url = reverse("register")


    def test_register_user_successfully(self):
        payload = {
            "email": "tej@example.com",
            "first_name": "Tej",
            "last_name": "R",
            "password": "StrongPassword123",
        }

        response = self.client.post(
            self.url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            User.objects.filter(
                email=payload["email"]
            ).exists()
        )

        user = User.objects.get(
            email=payload["email"]
        )

        self.assertTrue(
            user.check_password(payload["password"])
        )

        self.assertEqual(
            response.data["email"],
            payload["email"]
        )

        self.assertNotIn(
            "password",
            response.data,
        )

    
    def test_register_fails_with_duplicate_email(self):
        User.objects.create_user(
            email = "tej@example.com",
            first_name = "Tej",
            last_name = "R",
            password = "StrongPassword123",    
        )

        payload = {
            "email": "tej@example.com",
            "first_name": "Tej",
            "last_name": "R",
            "password": "StrongPassword123",
        }

        response = self.client.post(
            self.url,
            payload,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertEqual(
            User.objects.filter(
                email=payload["email"]
            ).count(),
            1,
        )

    
    def test_register_fails_with_invalid_email(self):
        payload = {
            "email": "invalid-email",
            "first_name": "Tej",
            "last_name": "R",
            "password": "strongpassword"
        }

        response = self.client.post(
            self.url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertIn(
            "email",
            response.data,
        )

        self.assertFalse(
            User.objects.filter(
                email=payload["email"],
            ).exists()
        )


    def test_register_fails_with_short_password(self):
        payload = {
            "email": "tej@example.com",
            "first_name": "Tej",
            "last_name": "R",
            "password": "strong"
        }

        response = self.client.post(
            self.url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertIn(
            "password",
            response.data,
        )

        self.assertFalse(
            User.objects.filter(
                email=payload["email"],
            ).exists()
        )

    
    def test_register_fails_when_last_name_is_missing(self):
        payload = {
            "email": "tej@example.com",
            "first_name": "Tej",
            "password": "strongpassword",
        }

        response = self.client.post(
            self.url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertIn(
            "last_name",
            response.data
        )

        self.assertFalse(
            User.objects.filter(
                email=payload["email"],
            ).exists()
        )

            

