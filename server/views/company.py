from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from server.lib.create import do_create_company
from server.models import Company
import json

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
