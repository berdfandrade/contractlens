import pytest
from unittest.mock import AsyncMock, patch
from app.services.mail import MailService


@pytest.mark.asyncio
async def test_send_email_with_html_adds_alternative():

    mail_service = MailService(
        host="localhost",
        port=1025,
        username="test@test.com",
        password="123456",
        use_tls=False,
    )

    with patch("app.services.mail.SMTP") as mock_smtp:

        mock_instance = AsyncMock()
        mock_smtp.return_value = mock_instance

        await mail_service.send_email(
            to="user@email.com",
            subject="Test Subject",
            text="Plain text",
            html="<h1>HTML</h1>",
        )

        sent_message = mock_instance.send_message.call_args[0][0]

        assert sent_message["Subject"] == "Test Subject"
        assert sent_message["To"] == "user@email.com"

        assert sent_message.is_multipart()

        parts = sent_message.get_payload()

        assert parts[0].get_content_type() == "text/plain"
        assert parts[1].get_content_type() == "text/html"
