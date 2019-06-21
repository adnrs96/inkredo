from django.contrib.auth.password_validation import validate_password
from django.http import HttpRequest, HttpResponse, JsonResponse
from server.lib.create import do_create_user
from server.models import User
from server.actions import get_user_by_id, get_company_by_id
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
    elif request.method == 'DELETE':
        if not request.user.is_authenticated or request.user.id != user_id:
            res = JsonResponse({'msg': 'Access Denied.'})
            res.status_code = 403
            return res
        user = get_user_by_id(user_id)
        if user is None:
            res = JsonResponse({'msg': 'Invalid user id'})
            res.status_code = 400
            return res

        try:
            user.delete()
        except Error as e:
            logging.error(e)
            res = JsonResponse({'msg': 'Something went wrong while attempting to delete!'})
            res.status_code = 500
            return res

        res = JsonResponse({'msg': 'success'})
        res.status_code = 200
        return res
    elif request.method == 'PATCH':
        if not request.user.is_authenticated or request.user.id != user_id:
            res = JsonResponse({'msg': 'Access Denied.'})
            res.status_code = 403
            return res
        user = get_user_by_id(user_id)
        if user is None:
            res = JsonResponse({'msg': 'Invalid user id'})
            res.status_code = 400
            return res

        try:
            patch_data = json.loads(request.body)
        except json.decoder.JSONDecodeError:
            res = JsonResponse({'msg': 'Invalid JSON Body.'})
            res.status_code = 400
            return res

        # We construct this API to update only one field via one request.
        field_to_update = patch_data.get('update_field', '')
        updated_value = patch_data.get('update_value', '')
        if field_to_update not in ('full_name', 'company_id'):
            res = JsonResponse({'msg': 'Given field cannot be updated.'})
            res.status_code = 403
            return res

        if field_to_update == 'company_id':
            company = get_company_by_id(updated_value)
            if company is not None:
                user.company = company
            else:
                res = JsonResponse({'msg': 'Given Company does not exist.'})
                res.status_code = 403
                return res
        else:
            setattr(user, field_to_update, updated_value)

        try:
            user.save()
        except Error as e:
            logging.error(e)
            res = JsonResponse({'msg': 'Something went wrong while attempting to update!'})
            res.status_code = 500
            return res

        res = JsonResponse({'msg': 'success'})
        res.status_code = 200
        return res
    else:
        res = JsonResponse({'msg': 'Only GET requests accepted.'})
        res.status_code = 405
        return res
