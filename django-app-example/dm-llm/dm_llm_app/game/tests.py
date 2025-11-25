"""Tests for Dungeon Master API endpoints."""

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class DungeonAPITestCase(APITestCase):
    """Test case for Dungeon Master API endpoints."""

    def setUp(self):
        """Set up test fixtures."""
        self.url = reverse("dungeon")
        self.valid_payload = {
            "world_context": "A mysterious enchanted forest",
            "genre": "Fantasy",
            "difficulty": "Medium",
            "narrative_tone": "Dramatic",
            "campaign_name": "Enchanted Quest",
            "user_question": "What lies ahead on the path?",
        }

    def test_dungeon_endpoint_valid(self):
        """Test dungeon endpoint with valid payload."""
        response = self.client.post(self.url, self.valid_payload, format="json")
        # Check if the response contains a narrative (in our test, we might simulate a response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("narrative", response.data)

    def test_dungeon_endpoint_missing_field(self):
        """Test dungeon endpoint with missing required field."""
        invalid_payload = self.valid_payload.copy()
        del invalid_payload["user_question"]
        response = self.client.post(self.url, invalid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
