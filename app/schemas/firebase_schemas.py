from pydantic import BaseModel


class FirebaseTokenRequest(BaseModel):
    id_token: str # The Firebase ID token sent from the frontend

# Assuming your authentication response involves a User schema and an access token
class AuthSuccessResponse(BaseModel):
    user: dict # Or replace with your User schema if defined
    access_token: str


