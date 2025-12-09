from infrastructure.notification.smtp_service import SmtpService


class EmailCodeService:
    def __init__(self, smtp_service: SmtpService):
        self.smtp_service = smtp_service

    def send_code(self, email: str, email_code: str):
        body = f"""
        Здравствуйте! Ваш код для входа в систему Scaniq:
        {email_code}
        Если вы не запрашивали данный код, то проигнорируйте это письмо."""
        self.smtp_service.send_email(email, "Вход в систему Scaniq", body)

