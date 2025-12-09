import smtplib
from email.message import EmailMessage

from core.config import SmtpConfig


class SmtpService:
    def __init__(self, smtp_config: SmtpConfig):
        self.smtp_config = smtp_config

    def send_email(self, to: str, subject: str, body: str):
        message = EmailMessage()
        message["Subject"] = subject
        message["From"] = self.smtp_config.smtp_user
        message["To"] = to
        message.set_content(body, subtype="html")

        with smtplib.SMTP_SSL(self.smtp_config.smtp_host, self.smtp_config.smtp_port) as smtp:
            smtp.login(self.smtp_config.smtp_user, self.smtp_config.smtp_password)
            smtp.send_message(message)
