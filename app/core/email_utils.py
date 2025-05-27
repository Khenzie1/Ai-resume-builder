import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings
import logging
from fastapi import HTTPException


def send_reset_email(to_email: str, reset_link: str):
    smtp_server = settings.MAIL_SERVER
    smtp_port = settings.MAIL_PORT
    smtp_user = settings.MAIL_USERNAME
    smtp_password = settings.MAIL_PASSWORD
    from_email = settings.MAIL_FROM

    print(f"[DEBUG] SMTP server: {smtp_server}")
    print(f"[DEBUG] SMTP port: {smtp_port}")
    print(f"[DEBUG] From: {from_email}")
    print(f"[DEBUG] To: {to_email}")

    message = MIMEMultipart("alternative")
    message["Subject"] = "Password Reset Request"
    message["From"] = from_email
    message["To"] = to_email

    text = f"""
Hi,

You requested to reset your password. Click the link below to reset it:

{reset_link}

If you did not request this, please ignore this email.

Thanks.
"""
    part = MIMEText(text, "plain")
    message.attach(part)

    try:
        if smtp_port == 465:
            with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                server.login(smtp_user, smtp_password)
                server.sendmail(from_email, to_email, message.as_string())
        elif smtp_port == 587:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_password)
                server.sendmail(from_email, to_email, message.as_string())
        else:
            raise HTTPException(status_code=500, detail=f"Unsupported SMTP port: {smtp_port}")

        logging.info(f"Password reset email sent to {to_email}")

    except Exception as e:
        logging.error(f"SMTP Error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to send reset email. Reason: {str(e)}")
