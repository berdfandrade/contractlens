import pytest
from unittest.mock import AsyncMock, patch
from app.services.mail import MailService


@pytest.mark.asyncio
async def test_send_email_calls_smtp_methods():

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
            body="Test Body",
        )

        mock_instance.connect.assert_called_once()
        mock_instance.login.assert_called_once_with("test@test.com", "123456")
        mock_instance.send_message.assert_called_once()
        mock_instance.quit.assert_called_once()
