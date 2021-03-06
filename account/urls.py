from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^timein/$', views.time_in, name='time_in'),
    url(r'^timeout/$', views.time_out, name='time_out'),
    url(r'^attendance/status/$', views.attendance_status, name='attendance_status'),
]
