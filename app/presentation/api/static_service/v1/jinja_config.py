from pathlib import Path

from fastapi.templating import Jinja2Templates


templates_path = Path(__file__).parent / "templates"
templates = Jinja2Templates(directory=str(templates_path))
