import json
import datetime

from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from .decorators import require_json_data
from .models import Attendance

from pytz import timezone


JSON = "application/json"

def index(request):
    pass

@require_http_methods(['POST'])
@require_json_data
def time_in(request):
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')

    user = authenticate(username=username, password=password)
    if user is None or not user.is_active:
        return HttpResponse(status=401)

    attendance = Attendance(user=user)
    attendance.time_in = datetime.datetime.now(tz=timezone('UTC')).time()
    attendance.save()

    return HttpResponse(status=200)

@require_http_methods(['POST'])
@require_json_data
def time_out(request):
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')

    user = authenticate(username=username, password=password)
    if user is None or not user.is_active:
        return HttpResponse(status=401)

@require_http_methods(['GET'])
def attendance_status(request):
    attendances = Attendance.objects.select_related('user').filter(user__is_active=True)
    data = {}
    for attendance in attendances:
        if not attendance.user.id in data.keys():
            data[attendance.user.id] = {
                'username':attendance.user.username,
                'attendance':[{
                    'time_in':attendance.time_in,
                    'time_out':attendance.time_out
                }]
            }
        else:
            data[attendance.user.id]['attendance'].append({
                'time_in':attendance.time_in,
                'time_out':attendance.time_out
            })
    
    print data

    return HttpResponse(status=200, content_type=JSON)
