from core.page import setup_page
from ui.views import render_registration_screen

setup_page(
    logger_name=__name__,
    page_title="Cadastro",
    screen_title="Cadastro de Conjunto",
    layout="centered",
    log_message="Renderizando tela: Cadastro de Conjunto",
)
render_registration_screen()
