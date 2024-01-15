from pydantic import BaseModel, ValidationError, validator, Field, EmailStr
from  typing import Optional

class CustomBaseModel(BaseModel):
    id: int = Field(gt=0)
    name: str = Field(min_length=1)

class User(CustomBaseModel):
    email: EmailStr

class Category(CustomBaseModel):
    priority: str

class Task(CustomBaseModel):
    description: str = Field('Does not contain any description', min_length=10)
    test: Optional[str] = Field('')
    is_active: bool
    user: User
    category: Category