import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
GMAIL_EMAIL = os.getenv("GMAIL_EMAIL")
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")


def send_registration_email(to_email: str, username: str):
    html = f"""
    <html>
        <body style="font-family: Arial; padding: 20px;">
            <h2>Welcome, {username}!</h2>
            <p>Your admin account has been successfully registered.</p>
            <p>You can now log in using your email and password.</p>
            <p>Best regards,<br>Delivery Tracking System</p>
        </body>
    </html>
    """
    
    msg = MIMEMultipart('alternative')
    msg['From'] = GMAIL_EMAIL
    msg['To'] = to_email
    msg['Subject'] = "Admin Registration Successful"
    msg.attach(MIMEText(html, 'html'))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(GMAIL_EMAIL, GMAIL_PASSWORD)
        server.send_message(msg)


def send_login_otp_email(to_email: str, otp: str):
    html = f"""
    <html>
        <body style="font-family: Arial; padding: 20px;">
            <h2>Your Login OTP</h2>
            <p style="font-size: 24px; color: #2196F3; font-weight: bold; letter-spacing: 2px;">{otp}</p>
            <p>This OTP will expire in 10 minutes.</p>
            <p style="color: #999; font-size: 12px;">Never share this OTP with anyone.</p>
        </body>
    </html>
    """
    
    msg = MIMEMultipart('alternative')
    msg['From'] = GMAIL_EMAIL
    msg['To'] = to_email
    msg['Subject'] = "Your Login OTP"
    msg.attach(MIMEText(html, 'html'))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(GMAIL_EMAIL, GMAIL_PASSWORD)
        server.send_message(msg)

def send_email_to_driver(to_email: str, name: str, password: str):
    html = f"""
    <html>
        <body style="font-family: Arial; padding: 20px;">
            <h2>Welcome, {name}!</h2>
            <p>Your driver account has been successfully created.</p>
            <p>Your login credentials are as follows:</p>
            <ul>
                <li><strong>Email:</strong> {to_email}</li>
                <li><strong>Password:</strong> {password}</li>
            </ul>
            <p>Please change your password after your first login.</p>
            <p>Best regards,<br>Delivery Tracking System</p>
        </body>
    </html>
    """
    
    msg = MIMEMultipart('alternative')
    msg['From'] = GMAIL_EMAIL
    msg['To'] = to_email
    msg['Subject'] = "Driver Account Created"
    msg.attach(MIMEText(html, 'html'))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(GMAIL_EMAIL, GMAIL_PASSWORD)
        server.send_message(msg)