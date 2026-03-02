from email.message import EmailMessage
from aiosmtplib import SMTP


class MailService:
    def __init__(
        self, host: str, port: int, username: str, password: str, use_tls=True
    ):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.use_tls = use_tls

    async def send_email(
        self,
        to: str,
        subject: str,
        text: str,
        html: str | None = None,
    ):
        message = EmailMessage()
        message["From"] = self.username
        message["To"] = to
        message["Subject"] = subject

        message.set_content(text)

        if html:
            message.add_alternative(html, subtype="html")

        smtp = SMTP(hostname=self.host, port=self.port, start_tls=self.use_tls)
        await smtp.connect()
        await smtp.login(self.username, self.password)
        await smtp.send_message(message)
        await smtp.quit()
