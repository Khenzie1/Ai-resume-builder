import os
import firebase_admin
from firebase_admin import credentials, auth
from app.core.config import settings

firebase_credentials_path = settings.GOOGLE_APPLICATION_CREDENTIALS

if not firebase_credentials_path:
    raise ValueError("GOOGLE_APPLICATION_CREDENTIALS is not set in the .env file")

# Convert to absolute path if necessary
firebase_credentials_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", firebase_credentials_path)
) if not os.path.isabs(firebase_credentials_path) else firebase_credentials_path

if not os.path.exists(firebase_credentials_path):
    raise FileNotFoundError(f"Firebase credentials file not found at: {firebase_credentials_path}")

# Initialize Firebase Admin SDK only once
if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_credentials_path)
    firebase_admin.initialize_app(cred)
