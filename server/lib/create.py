from typing import Optional
from server.models import Company
from django.db import Error

def do_create_company(name: str,
                      email: str,
                      registered_name: str,
                      address: str,
                      type: int=Company.PRIVATE) -> Optional[Company]:
    try:
        company = Company(name=name,
                          email=email,
                          registered_name=registered_name,
                          address=address,
                          type=type)
        company.save()
    except Error:
        return None
    return company
