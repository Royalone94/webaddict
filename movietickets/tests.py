from django.test import TestCase
from django.contrib.auth.models import User
# Create your tests here.
from unittest.mock import patch
from rest_framework.test import APITestCase
from rest_framework import status


class MovieTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user('user', 'user@example.com', 'user')
        self.client.force_authenticate(user=self.user)

    def test_get_movies(self):
        response = self.client.get(
            '/api/movies/',
            format='json'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_get_tickets(self):
        response = self.client.get(
            '/api/tickets/',
            format='json'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_get_my_tickets(self):
        response = self.client.get(
            '/api/tickets/get_my_tickets/',
            format='json'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )