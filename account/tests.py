from django.test import TestCase
from .models import *


class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create(password='1234')

    def test_invalid_password(self): 
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(pk=1, password='123')
