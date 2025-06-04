import smtplib
from email.mime.text import MIMEText
from app.core.config import settings

# Changed 'token' to 'code' in the function signature
def send_reset_email(to_email: str, code: str):
    subject = "Your Password Reset Code"
    # The email body now includes the 6-digit code
    body = f"Your password reset code is: {code}\n\n"
    #This code is valid for 20 minutes. Please enter this code on the password reset page to set your new password."
    
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = settings.MAIL_USERNAME
    msg["To"] = to_email

    try:
        print("Connecting to email server...")
        with smtplib.SMTP_SSL(settings.MAIL_SERVER, 465) as server:
            server.login(settings.MAIL_USERNAME, settings.MAIL_PASSWORD)
            server.sendmail(settings.MAIL_USERNAME, to_email, msg.as_string())
        print("Email sent!")
    except Exception as e:
        print("Failed to send email:", e)

#To enable sending pdf to user's Emails
# from celery import Celery
from fastapi import BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from fastapi.responses import JSONResponse
# from email.message import EmailMessage
from app.schemas.email_schema import EmailSchema, ContactSchema
from fastapi import APIRouter

router = APIRouter()

#Celery configuration
# celery = Celery("tasks", broker="amqp://guest@localhost//")


#Celery task to send Email
# @celery.task
conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS
)
def send_email_background(background_tasks:BackgroundTasks, email:str, resume:str):
    message = MessageSchema(
    subject= "Resume",
    recipients=[email],
    body=resume,
    subtype="plain",
    )
    fm = FastMail(conf)
    background_tasks.add_task(fm.send_message, message)

#Endpoint to send resume to email
@router.post("/send-resume")
async def send_resume(email:EmailSchema, background_tasks:BackgroundTasks):
    send_email_background(background_tasks, email.email, email.resume)
    return JSONResponse(status_code=200, content={"message":"Email sent successfully"})


#send email to user
def send_email_to_user(email:ContactSchema):
    message = MessageSchema(
    subject= "Contact",
    recipients=[email],
    body=message,
    subtype="plain",
    )

@router.post("/contact")
async def contact_user(contact:ContactSchema, background_tasks:BackgroundTasks):
    send_email_to_user(background_tasks,contact.name, contact.email, contact.message)
    return JSONResponse(status_code=200, content={"message":"Email sent successfully"})
# @celery.task
# def send_email_to_user(email:ContactSchema):
#     msg = EmailMessage
#     msg.set_content(email.message)
#     msg["Subject"] = "Contact"
#     msg["From"] = settings.MAIL_FROM
#     msg["To"] = email.email


# @router.post("/contact")
# async def contact_user(contact:ContactSchema):
#     send_email_to_user.delay(contact.name, contact.email, contact.message)
#     return JSONResponse(status_code=200, content={"message":"Email sent successfully"})