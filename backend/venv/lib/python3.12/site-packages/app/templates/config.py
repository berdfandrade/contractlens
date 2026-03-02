from fastapi.templating import Jinja2Templates
from app.core.config import template_settings


templates = Jinja2Templates(directory=str(template_settings.TEMPLATE_DIR))
