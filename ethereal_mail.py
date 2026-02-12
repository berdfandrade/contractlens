from aiosmtplib import SMTP
import asyncio
from email.message import EmailMessage
from aiosmtplib import SMTP

import aiosmtplib

async def create_ethereal_account():
    import requests

    # Ethereal fornece API para criar contas de teste
    resp = requests.post("https://api.nodemailer.com/user")
    data = resp.json()
    print(data)
    return data

asyncio.run(create_ethereal_account())

