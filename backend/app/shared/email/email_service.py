import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class EmailService:
    def __init__(self):
        self._is_production = os.getenv("FLASK_ENV") == "production"
        self._from_address = os.getenv("MAIL_FROM")
        self._from_name = os.getenv("MAIL_FROM_NAME", "Flight Tracker")

    def _get_smtp_config(self) -> dict:
        if self._is_production:
            return {
                "host": os.getenv("GMAIL_HOST"),
                "port": int(os.getenv("GMAIL_PORT", 587)),
                "username": os.getenv("GMAIL_USERNAME"),
                "password": os.getenv("GMAIL_PASSWORD"),
            }
        return {
            "host": os.getenv("MAILTRAP_HOST"),
            "port": int(os.getenv("MAILTRAP_PORT", 2525)),
            "username": os.getenv("MAILTRAP_USERNAME"),
            "password": os.getenv("MAILTRAP_PASSWORD"),
        }

    def send(self, to: str, subject: str, html: str) -> None:
        config = self._get_smtp_config()

        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = f"{self._from_name} <{self._from_address}>"
        message["To"] = to
        message.attach(MIMEText(html, "html"))

        with smtplib.SMTP(config["host"], config["port"]) as server:
            server.starttls()
            server.login(config["username"], config["password"])
            server.sendmail(self._from_address, to, message.as_string())