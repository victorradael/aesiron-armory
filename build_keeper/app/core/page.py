import streamlit as st

from core.logger import get_logger
from core.settings import get_settings
from ui.styles import apply_custom_css


def setup_page(
    *,
    logger_name: str,
    page_title: str,
    screen_title: str = "",
    layout: str = "centered",
    subtitle: str = "",
    log_message: str,
) -> None:
    settings = get_settings()
    logger = get_logger(logger_name)

    st.set_page_config(page_title=f"{page_title} - {settings.app_name}", layout=layout)
    apply_custom_css()
    st.title(screen_title or settings.app_name)

    if subtitle:
        st.subheader(subtitle)

    logger.info(log_message)
