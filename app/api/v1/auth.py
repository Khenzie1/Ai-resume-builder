from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserLogin, UserOut
from app.crud import user as crud_user
from app.core.security import verify_password, create_access_token
from app.api.deps import get_db

router = APIRouter()

@router.post("/register", response_model=UserOut)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_email(db, email=user_data.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud_user.create_user(db, user=user_data)

@router.post("/login")  
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = crud_user.get_user_by_email(db, email=user_data.email)
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}






#THE ONE THAT IS NOT RUNNING AT ALL AND CAUSING ERRORS 
# SO DON'T UNCOMMENT TOMMORROW




# from fastapi import APIRouter, Depends, HTTPException, Request, status
# from fastapi.security import OAuth2PasswordRequestForm
# from sqlalchemy.orm import Session
# from firebase_admin import auth as firebase_auth
# from app.core.firebase import *  # initializes Firebase
# from app.core.config import settings
# # from app.core.oauth import oauth  # if you still want Google OAuth via redirect
# from app.schemas.user import UserCreate, UserLogin
# from app.crud import user as user_crud
# from app.db.session import get_db

# router = APIRouter()


# @router.post("/register")
# def register(user: UserCreate, db: Session = Depends(get_db)):
#     db_user = user_crud.get_user_by_email(db, email=user.email)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     new_user = user_crud.create_user(db, email=user.email, password=user.password)
#     return {"message": "User created successfully", "user": new_user.email}


# @router.post("/login")
# def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
#     user = user_crud.authenticate_user(db, email=form_data.username, password=form_data.password)
#     if not user:
#         raise HTTPException(status_code=401, detail="Invalid credentials")
#     access_token = user_crud.create_access_token(data={"sub": user.email})
#     return {"access_token": access_token, "token_type": "bearer"}


# @router.post("/firebase-login")
# async def firebase_login(request: Request, db: Session = Depends(get_db)):
#     body = await request.json()
#     id_token = body.get("token")

#     if not id_token:
#         raise HTTPException(status_code=400, detail="Token is required")

#     try:
#         decoded_token = firebase_auth.verify_id_token(id_token)
#         email = decoded_token.get("email")
#         name = decoded_token.get("name")

#         if not email:
#             raise HTTPException(status_code=400, detail="Email not found in Firebase token")

#         user = user_crud.get_user_by_email(db, email=email)
#         if not user:
#             user = user_crud.create_user(db, email=email, password=None)

#         access_token = user_crud.create_access_token(data={"sub": user.email})
#         return {"access_token": access_token, "token_type": "bearer"}
#     except Exception as e:
#         raise HTTPException(status_code=401, detail=f"Invalid Firebase token: {str(e)}")


# @router.get("/google/login")
# async def google_login(request: Request):
#     redirect_uri = settings.GOOGLE_OAUTH_REDIRECT_URI
#     return await oauth.google.authorize_redirect(request, redirect_uri)


# @router.get("/google/callback")
# async def google_callback(request: Request, db: Session = Depends(get_db)):
#     try:
#         token = await oauth.google.authorize_access_token(request)
#         user_info = await oauth.google.parse_id_token(request, token)
#     except Exception:
#         raise HTTPException(status_code=400, detail="Google OAuth authorization failed")

#     if not user_info or "email" not in user_info:
#         raise HTTPException(status_code=400, detail="Invalid user info from Google")

#     email = user_info["email"]
#     user = user_crud.get_user_by_email(db, email=email)
#     if not user:
#         user = user_crud.create_user(db, email=email, password=None)

#     access_token = user_crud.create_access_token(data={"sub": user.email})
#     return {"access_token": access_token, "token_type": "bearer"}



# from fastapi import APIRouter, Depends, HTTPException, Request, status
# from fastapi.security import OAuth2PasswordRequestForm
# from sqlalchemy.orm import Session
# from firebase_admin import auth as firebase_auth
# from app.core.firebase import *  # initializes Firebase
# from app.core.config import settings
# from app.schemas.user import UserCreate, UserLogin
# from app.crud import user as user_crud
# from app.db.session import get_db

# router = APIRouter()

# @router.post("/register")
# def register(user: UserCreate, db: Session = Depends(get_db)):
#     db_user = user_crud.get_user_by_email(db, email=user.email)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     new_user = user_crud.create_user(db, email=user.email, password=user.password)
#     return {"message": "User created successfully", "user": new_user.email}

# @router.post("/login")
# def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
#     user = user_crud.authenticate_user(db, email=form_data.username, password=form_data.password)
#     if not user:
#         raise HTTPException(status_code=401, detail="Invalid credentials")
#     access_token = user_crud.create_access_token(data={"sub": user.email})
#     return {"access_token": access_token, "token_type": "bearer"}

# @router.post("/firebase-login")
# async def firebase_login(request: Request, db: Session = Depends(get_db)):
#     body = await request.json()
#     id_token = body.get("token")

#     if not id_token:
#         raise HTTPException(status_code=400, detail="Token is required")

#     try:
#         decoded_token = firebase_auth.verify_id_token(id_token)
#         email = decoded_token.get("email")
#         name = decoded_token.get("name")

#         if not email:
#             raise HTTPException(status_code=400, detail="Email not found in Firebase token")

#         user = user_crud.get_user_by_email(db, email=email)
#         if not user:
#             user = user_crud.create_user(db, email=email, password=None)

#         access_token = user_crud.create_access_token(data={"sub": user.email})
#         return {"access_token": access_token, "token_type": "bearer"}
#     except Exception as e:
#         raise HTTPException(status_code=401, detail=f"Invalid Firebase token: {str(e)}")
