from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

import hashlib


class UserTest(TestCase):

    login_url = reverse('account:login')

    def setUp(self):
        pass

    def test_login_invalid_json_post_data(self):
        request = {'username':'admin', 'password':'admin'}
        client = Client()
        response = client.post(self.login_url, request)

        self.assertEquals(response.status_code, 400)

    def test_login_invalid_http_method(self):
        client = Client()
        response = client.get(self.login_url)

        self.assertEquals(response.status_code, 405)

    def test_login_invalid_user(self):
        request = '{"username":"user", "password":"user"}'
        client = Client()
        response = client.post(self.login_url, request, content_type="application/json")

        self.assertEquals(response.status_code, 401)

    def test_login_disabled_user(self):
        user = User.objects.create_user('user', password='user')
        user.is_active = False
        user.save()

        request = '{"username":"user", "password":"user"}'
        client = Client()
        response = client.post(self.login_url, request, content_type="application/json")

        self.assertEquals(response.status_code, 401)

    def test_login_valid_user(self):
        user = User.objects.create_user('user', password='user')

        request = '{"username":"user", "password":"user"}'
        client = Client()
        response = client.post(self.login_url, request, content_type="application/json")

        self.assertEquals(response.status_code, 200)
