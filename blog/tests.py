from django.test import TestCase, Client
from django.urls import reverse


class BlogTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_blog_title(self):
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'BallN')
