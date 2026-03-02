from app.services.mail import MailService
from app.core.config import settings
import asyncio


async def main():
    mail_service = MailService(
        host="smtp.ethereal.email",
        port=587,
        username="richard.strosin72@ethereal.email",
        password="UemmyGrFeBPhef3rGN",
        use_tls=True,
    )

    await mail_service.send_email(
        to="berdfandrade@gmail.com",
        subject="Teste Ethereal",
        body="<h1>Olá, mundo!</h1><p>Esse é um email de teste.</p>",
        html=True,
    )


asyncio.run(main())
