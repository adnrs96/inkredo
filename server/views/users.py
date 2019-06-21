from django.contrib.auth.password_validation import validate_password
from django.http import HttpRequest, HttpResponse, JsonResponse
from server.lib.create import do_create_user
from server.models import User
from server.actions import get_user_by_id
from django.core.exceptions import ValidationError
from django.db import Error
import json
import logging

def create_user_endpoint(request: HttpRequest) -> HttpResponse:
    if request.method != 'POST':
        res = JsonResponse({'msg': 'Only POST requests accepted.'})
        res.status_code = 405
        return res

    try:
        user_to_create = json.loads(request.body)
    except json.decoder.JSONDecodeError:
        res = JsonResponse({'msg': 'Invalid JSON Body.'})
        res.status_code = 400
        return res

    name = user_to_create.get('full_name', '')
    email = user_to_create.get('email', '')
    username = user_to_create.get('username', '')
    password = user_to_create.get('password', '')
    company_id = user_to_create.get('company_id', '')

    try:
        validate_password(password)
    except ValidationError:
        res = JsonResponse({'msg': 'Password not strong enough.'})
        res.status_code = 400
        return res

    new_user = do_create_user(name, email, username, password, company_id)
    if new_user is None:
        res = JsonResponse({'msg': 'One or more fields are either missing or not acceptable.'})
        res.status_code = 400
        return res

    res = JsonResponse({'msg': 'success', 'user_id': new_user.id})
    res.status_code = 200
    return res

def handle_user_endpoint(request: HttpRequest, user_id: int) -> HttpResponse:
    if request.method == 'GET':
        user = get_user_by_id(user_id)
        if user is None:
            res = JsonResponse({'msg': 'Invalid user id'})
            res.status_code = 400
            return res

        data = {
        	"full_name": user.full_name,
        	"email": user.email,
        	"username": user.username,
        	"company": user.company.id,
        }
        res = JsonResponse({'msg': 'success', 'user': data})
        res.status_code = 200
        return res
    else:
        res = JsonResponse({'msg': 'Only GET requests accepted.'})
        res.status_code = 405
        return res
