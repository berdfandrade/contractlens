from fastapi.staticfiles import StaticFiles
from app.core.config import template_settings


def mount_static(app):
    """
    Faz o mount da pasta de arquivos estáticos no app.
    """
    app.mount(
        template_settings.STATIC_URL,
        StaticFiles(directory=str(template_settings.STATIC_DIR)),
        name=template_settings.STATIC_NAME,
    )
