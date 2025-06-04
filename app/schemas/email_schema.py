from pydantic import BaseModel,EmailStr

class EmailSchema(BaseModel):
    email:EmailStr
    resume:str

class ContactSchema(BaseModel):
    name:str
    email:EmailStr
    message:str