# src/app/email_utils.py

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.core.config import settings

MAILTRAP_HOST = settings.email_host
MAILTRAP_PORT = settings.email_port
MAILTRAP_USER = settings.email_host_user
MAILTRAP_PASSWORD = settings.email_host_password
FROM_EMAIL = settings.email_from


def send_verification_email(to_email: str, token: str):
    verification_url = f"http://localhost:8000/verify-email?token={token}"

    # Create a multipart message
    msg = MIMEMultipart()
    msg["From"] = FROM_EMAIL
    msg["To"] = to_email
    msg["Subject"] = "Verify your email"

    body = f"""
    Hi,

    Thank you for registering. Click the link below to verify your email:

    {verification_url}

    This link will expire in 24 hours.
    """
    msg.attach(MIMEText(body, "plain"))

    # Send email via SMTP
    try:
        with smtplib.SMTP(MAILTRAP_HOST, MAILTRAP_PORT) as server:
            server.starttls()
            server.login(MAILTRAP_USER, MAILTRAP_PASSWORD)
            server.sendmail(FROM_EMAIL, to_email, msg.as_string())
            print(f"Email sent to {to_email} via Mailtrap SMTP")
    except Exception as e:
        print("Error sending email:", e)
