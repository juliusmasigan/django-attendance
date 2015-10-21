from django.db import models


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

    name = models.CharField(max_length=500)
    address = models.CharField(max_length=500)
    birth_date = models.DateField('Birthday')
    gender = models.CharField(max_length=1, choices=gender_choices, default='M')
    department = models.ForeignKey(Department, related_name='departments')
    creation_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '%s' % (self.name,)

class User(models.Model):
    password = models.CharField(max_length=255)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '%s' % (self.login_id,)

class Attendance(models.Model):
    user = models.ForeignKey(User, related_name='users')
    date = models.DateField('Date', auto_now_add=True)
    time_in = models.TimeField('Time In', auto_now_add=True)
    time_out = models.TimeField('Time Out', auto_now_add=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '%s' % (self.user,)
