import firebase_admin
from firebase_admin import credentials
from app.core.config import settings # Assuming your settings object is named 'settings'

def initialize_firebase():
    """
    Initializes the Firebase Admin SDK.
    This function should be called once when the application starts.
    """
    firebase_credentials_path = settings.GOOGLE_APPLICATION_CREDENTIALS

    if not firebase_credentials_path:
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS is not set in .env file")

    # Ensure the path is correct if the app runs from a different directory
    # For a path relative to the project root, you might need:
    # import os
    # base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    # full_path = os.path.join(base_dir, firebase_credentials_path)

    # For now, let's assume direct path if .env is in root
    cred = credentials.Certificate(firebase_credentials_path)
    firebase_admin.initialize_app(cred)
    print("Firebase Admin SDK initialized successfully.")