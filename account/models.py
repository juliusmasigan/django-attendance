#Python modules
import hashlib

#Django modules
from django.db import models
from django.contrib.auth.models import User

class Department(models.Model):
    name = models.CharField(max_length=255)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '%s' % (self.name,)

class Profile(models.Model):
    gender_choices = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    user = models.ForeignKey(User, related_name='profile_users', verbose_name='name')
    address = models.TextField("home address")
    birth_date = models.DateField('Date of Birth')
    gender = models.CharField(max_length=1, choices=gender_choices, default='M')
    department = models.ForeignKey(Department, related_name='profile_departments')
    contact_number = models.CharField(max_length=255, null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)

class Attendance(models.Model):
    user = models.ForeignKey(User, related_name='attendance_users')
    date = models.DateField('Date', auto_now_add=True)
    time_in = models.TimeField('Time In', auto_now_add=True)
    time_out = models.TimeField('Time Out', auto_now_add=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '%s' % (self.user,)
