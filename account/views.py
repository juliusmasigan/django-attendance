import json

from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from account.decorators import require_json_data


def index(request):
    pass

@require_http_methods(['POST'])
@require_json_data
def login(request):
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')

    user = authenticate(username=username, password=password)
    if user is None or not user.is_active:
        return HttpResponse(status=401)
    else:
        return login(request, user)

    return HttpResponse(status=200)
