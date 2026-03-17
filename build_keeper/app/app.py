from core.config_manager import get_app_code
from core.page import setup_page
from ui.views import render_checklist_screen, render_sidebar_config

setup_page(
    logger_name=__name__,
    page_title="Build Keeper - Home",
    subtitle=f"-> `{get_app_code()}` <-",
    layout="centered",
    log_message="Renderizando tela: Checklist de Equipamentos",
)
render_sidebar_config()
render_checklist_screen()
