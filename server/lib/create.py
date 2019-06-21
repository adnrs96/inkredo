from typing import Optional
from server.models import Company, User
from django.db import Error
from server.actions import get_company_by_id

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

def do_create_user(full_name: str,
                   email: str,
                   username: str,
                   password: str,
                   company: int) -> Optional[User]:
    try:
        user = User(
            full_name=full_name,
            email=email,
            username=username,
            company=get_company_by_id(company)
        )
        user.set_password(password)
        user.save()
    except Error:
        return None
    return user
