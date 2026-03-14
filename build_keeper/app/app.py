from core.page import setup_page
from ui.views import render_checklist_screen

setup_page(
    logger_name=__name__,
    page_title="App",
    subtitle="Code SZC4RANH",
    layout="centered",
    log_message="Renderizando tela: Checklist de Equipamentos",
)
render_checklist_screen()
