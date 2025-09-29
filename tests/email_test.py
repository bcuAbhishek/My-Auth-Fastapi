from app.core.security import create_token
from app.services.email_service import send_verification_email

if __name__ == "__main__":
    test_email = "abhishek_24152353@sunway.edu.np"
    token = create_token({"sub": test_email})
    send_verification_email(test_email, token)
