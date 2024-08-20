from django.test import TestCase
from .views import index

class IndexViewTest(TestCase):
    def test_index_view_without_user(self):
        response = self.client.get('/handling/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'No user found')

    def test_index_view_with_user(self):
        session = self.client.session
        session['user'] = {'userinfo': {'email': 'test@example.com'}}
        session.save()
        response = self.client.get('/handling/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'test@example.com')

    def test_index_view_post(self):
        response = self.client.post('/handling/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'Posting data?!')


class LogoutViewTest(TestCase):
    def test_logout_view(self):
        response = self.client.get('/handling/logout/')
        self.assertEqual(response.status_code, 302)  
        self.assertTrue(response.url.startswith('https://'))  
        self.assertIn('auth0.com', response.url) 
        self.assertIn('returnTo', response.url)
        self.assertIn('client_id', response.url)