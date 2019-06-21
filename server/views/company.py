from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from server.lib.create import do_create_company
from server.models import Company
from server.actions import get_company_by_id
from django.db import Error
import json
import logging

# Create your views here.
def create_company_endpoint(request: HttpRequest) -> HttpResponse:
    if request.method != 'POST':
        res = JsonResponse({'msg': 'Only POST requests accepted.'})
        res.status_code = 405
        return res

    try:
        company_to_create = json.loads(request.body)
    except json.decoder.JSONDecodeError:
        res = JsonResponse({'msg': 'Invalid JSON Body.'})
        res.status_code = 400
        return res

    name = company_to_create.get('name', '')
    email = company_to_create.get('email', '')
    registered_name = company_to_create.get('registered_name', '')
    address = company_to_create.get('address', '')
    type = company_to_create.get('type', Company.PRIVATE)

    new_company = do_create_company(name, email, registered_name, address, type)
    if new_company is None:
        res = JsonResponse({'msg': 'One or more fields are either missing or not acceptable.'})
        res.status_code = 400
        return res

    res = JsonResponse({'msg': 'success', 'company_id': new_company.id})
    res.status_code = 200
    return res

def handle_company_endpoint(request: HttpRequest, company_id: int) -> HttpResponse:
    if request.method == 'GET':
        company = get_company_by_id(company_id)
        if company is None:
            res = JsonResponse({'msg': 'Invalid company id'})
            res.status_code = 400
            return res

        data = {
        	"name": company.name,
        	"registered_name": company.registered_name,
        	"address": company.address,
        	"type": company.type,
        	"email": company.email,
        }
        res = JsonResponse({'msg': 'success', 'company': data})
        res.status_code = 200
        return res
    elif request.method == 'DELETE':
        company = get_company_by_id(company_id)
        if company is None:
            res = JsonResponse({'msg': 'Invalid company id'})
            res.status_code = 400
            return res

        try:
            company.delete()
        except Error as e:
            logging.error(e)
            res = JsonResponse({'msg': 'Something went wrong while attempting to delete!'})
            res.status_code = 500
            return res

        res = JsonResponse({'msg': 'success'})
        res.status_code = 200
        return res
    else:
        res = JsonResponse({'msg': 'Only GET requests accepted.'})
        res.status_code = 405
        return res
