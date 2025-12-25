from pydantic import EmailStr, Field
from .api_base_model import TunedModel


# Admin Schemas
class AdminBase(TunedModel):
    email: EmailStr

class AdminCreate(AdminBase):
    admin_id: str = Field(..., max_length=8)
    password: str 

class Admin_Response(AdminBase):
    admin_id: str 

