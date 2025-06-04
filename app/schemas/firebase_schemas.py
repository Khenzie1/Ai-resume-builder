# app/schemas/firebase_schemas.py
from pydantic import BaseModel
from app.schemas.user import UserOut # <--- ADD THIS IMPORT!


class FirebaseTokenRequest(BaseModel):
    id_token: str

# Assuming your authentication response involves a User schema and an access token
class AuthSuccessResponse(BaseModel):
    user: UserOut # <--- CHANGE THIS FROM 'dict' TO 'UserOut'
    access_token: str