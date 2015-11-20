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
    users = User.objects.filter(is_active=True)
    user_list = []
    for user in users:
        user_list.append(user.username)
    attendances = Attendance.objects.filter(user__in=users)
    print attendances

    return HttpResponse(status=200, content_type=JSON)
