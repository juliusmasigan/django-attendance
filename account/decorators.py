import json

from django.http import HttpResponse


JSON = 'application/json'

def require_json_data(func):

    def _dec(request, *args, **kwargs):
        try:
            json.loads(request.body)
        except ValueError:
            content={
                'status_code':400,
                'message':'Malformed JSON data.',
            }
            return HttpResponse(
                status=400, 
                content=content,
                content_type=JSON)

        return func(request, *args, **kwargs)

    return _dec
