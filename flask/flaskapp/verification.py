from flask_mail import Mail, Message
from flask import current_app
import uuid

mail = Mail()

def init_mail(app):
    # Initialize Flask-Mail with the Flask application instance
    mail.init_app(app)

def generate_verification_token():
    # Generate a unique verification token (example: using UUID)
    return str(uuid.uuid4())

def send_verification_email(recipient, token):
    # Compose the verification email
    subject = "Email Verification"
    sender = current_app.config['MAIL_USERNAME']
    verification_link = f"{current_app.config['BASE_URL']}/verify_email?token={token}"
    body = f"Please click the following link to verify your email address: {verification_link}"

    # Send the email
    msg = Message(subject, sender=sender, recipients=[recipient])
    msg.body = body
    try:
        mail.send(msg)
        return True
    except Exception as e:
        # Handle email sending errors
        print(f"Error sending verification email: {e}")
        return False
