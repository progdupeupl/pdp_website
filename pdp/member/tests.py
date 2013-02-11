from django.test import TestCase
from models import Profile

class SimpleTest(TestCase):
    def test_index(self):
        resp = self.client.get('/membres/')
        self.assertEqual(resp.status_code, 200)
