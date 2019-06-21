from typing import Optional
from server.models import Company, User

def get_company_by_id(id: int) -> Optional[Company]:
    return Company.objects.filter(id=id).first()

def get_user_by_id(id: int) -> Optional[User]:
    return User.objects.filter(id=id).first()
