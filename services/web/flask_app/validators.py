from pydantic import BaseModel, Field, EmailStr


class RegistrationForm(BaseModel):
    username: str = Field(max_length=50)
    password: str = Field(max_length=120)
    email: EmailStr
