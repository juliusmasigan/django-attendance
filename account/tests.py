from django.test import TestCase, Client
from .models import User

import hashlib


class UserTest(TestCase):
    def setUp(self):
        pass

    def test_unknown_user(self):
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(pk=1)

    def test_invalid_password(self): 
        User.objects.create(password='1234')

        with self.assertRaises(User.DoesNotExist):
            md5 = hashlib.md5()
            md5.update('123')
            password = md5.hexdigest()
            User.objects.get(pk=1, password=password)

    def test_disabled_user(self):
        pass
