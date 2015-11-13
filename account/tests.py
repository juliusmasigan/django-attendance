import hashlib
import datetime

from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from .models import Attendance

from pytz import timezone


JSON = 'application/json'

class UserTest(TestCase):

    time_in_url = reverse('account:time_in')
    time_out_url = reverse('account:time_out')

    def setUp(self):
        self.user = User.objects.create_user('user', password='user')
        self.valid_username = 'user'
        self.valid_password = 'user'

    def test_time_in_invalid_json_post_data(self):
        request = {'username':'admin', 'password':'admin'}
        client = Client()
        response = client.post(self.time_in_url, request)

        self.assertEquals(response.status_code, 400)

    def test_time_in_invalid_http_method(self):
        client = Client()
        response = client.get(self.time_in_url)

        self.assertEquals(response.status_code, 405)

    def test_time_in_invalid_user(self):
        request = '{"username":"invalid_user", "password":"invalid_user"}'
        client = Client()
        response = client.post(self.time_in_url, request, content_type=JSON)

        self.assertEquals(response.status_code, 401)

    def test_time_in_disabled_user(self):
        username = 'user1'
        password = 'user1'
        user = User.objects.create_user(username, password=password)
        user.is_active = False
        user.save()

        request = '{"username":"{}", "password":"{}"}'.format(username, password)
        client = Client()
        response = client.post(self.time_in_url, request, content_type=JSON)

        self.assertEquals(response.status_code, 401)

    def test_time_in_valid_user(self):
        request = '{"username":"{}", "password":"{}"}'.format(self.valid_username, self.valid_password)
        client = Client()
        response = client.post(self.time_in_url, request, content_type=JSON)

        attendance = Attendance.objects.filter(user=user).order_by('-date_created')
        latest_attendance = attendance.first()

        self.assertEquals(response.status_code, 200)
        self.assertGreater(attendance.count(), 0)
        self.assertEqual(latest_attendance.date, datetime.datetime.now().date())
        self.assertIsNotNone(latest_attendance.time_in)
        self.assertIsNone(latest_attendance.time_out)

    def test_multiple_time_in(self):
        request = '{"username":"{}", "password":"{}"}'.format(self.valid_username, self.valid_password)
        client = Client()
        response = client.post(self.time_in_url, request, content_type=JSON)
        self.assertEquals(response.status_code, 200)
        response = client.post(self.time_in_url, request, content_type=JSON)
        self.assertEquals(response.status_code, 200)

        attendances = Attendance.objects.filter(user=user).order_by('-date_created')
        self.assertGreater(attendances.count(), 0)

        for attendance in attendances:
            self.assertEqual(attendance.date, datetime.datetime.now().date())
            self.assertIsNotNone(attendance.time_in)
            self.assertIsNone(attendance.time_out)
