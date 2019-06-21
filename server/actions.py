from typing import Optional
from server.models import Company

def get_company_by_id(id: int) -> Optional[Company]:
    return Company.objects.filter(id=id).first()
