from pydantic import BaseModel, Field, EmailStr

class CustomBaseModel(BaseModel):
    id: int = Field(gt=0)
    name: str = Field(min_length=1)

class User(CustomBaseModel):
    email: EmailStr

class Category(CustomBaseModel):
    priority: str

class Task(CustomBaseModel):
    description: str = Field('Does not contain any description', min_length=10)
    is_active: bool
    user: User
    category: Category