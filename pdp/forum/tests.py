from django.test import TestCase

class SimpleTest(TestCase):
    def test_index(self):
        resp = self.client.get('/forums/')
        self.assertEqual(resp.status_code, 200)
