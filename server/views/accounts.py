from django.contrib.auth import login, logout
from django.http import HttpRequest, HttpResponse, JsonResponse
from server.models import User
from server.actions import get_user_by_username
import json

def handle_login(request: HttpRequest) -> HttpResponse:
    if request.method != 'POST':
        res = JsonResponse({'msg': 'Only POST requests accepted.'})
        res.status_code = 405
        return res
    try:
        request_data = json.loads(request.body)
    except json.decoder.JSONDecodeError:
        res = JsonResponse({'msg': 'Invalid JSON Body.'})
        res.status_code = 400
        return res
    potential_user = get_user_by_username(request_data.get('username', ''))
    if potential_user is not None:
        authenticated = potential_user.check_password(request_data.get('password', ''))
        if authenticated:
            login(request, potential_user)
            res = JsonResponse({'msg': 'success'})
            res.status_code = 200
            return res
    res = JsonResponse({'msg': 'Either username or password is Invalid.'})
    res.status_code = 403
    return res
