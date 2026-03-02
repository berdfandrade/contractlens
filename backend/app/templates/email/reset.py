def reset_password_email_template(reset_link: str) -> dict:
    subject = "Redefinição de senha - Contract Lens"

    text = f"""
Você solicitou a redefinição de senha.

Clique no link abaixo:
{reset_link}

Se você não solicitou, ignore este e-mail.
"""

    html = f"""
    <div style="font-family: Arial, sans-serif;">
        <h2>Redefinição de senha</h2>
        <p>Você solicitou a redefinição de senha.</p>

        <a href="{reset_link}"
           style="
               display:inline-block;
               padding:12px 20px;
               background:#111;
               color:white;
               text-decoration:none;
               border-radius:6px;
           ">
           Redefinir senha
        </a>

        <p style="margin-top:20px;font-size:12px;color:gray;">
            Se você não solicitou, ignore este e-mail.
        </p>
    </div>
    """

    return {
        "subject": subject,
        "text": text,
        "html": html,
    }
