import smtplib
from email.mime.text import MIMEText
from app.core.config import settings

# Changed 'token' to 'code' in the function signature
def send_reset_email(to_email: str, code: str):
    subject = "Your Password Reset Code"
    # The email body now includes the 6-digit code
    body = f"Your password reset code is: {code}\n\nThis code is valid for 20 minutes. Please enter this code on the password reset page to set your new password."
    
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