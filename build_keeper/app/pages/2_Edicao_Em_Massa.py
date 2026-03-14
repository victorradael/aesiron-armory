import streamlit as st
from core.equipment_catalog import EQUIPMENT_TYPES
from core.equipment_manager import build_bulk_edit_rows, bulk_update_from_dataframe, load_equipment_sets
from core.page import setup_page

setup_page(
    logger_name=__name__,
    page_title="Edição em Massa",
    screen_title="📝 Edição em Massa",
    layout="wide",
    log_message="Renderizando tela: Edição em Massa",
)


def _build_column_config():
    column_config = {
        "id": None,
        "Nome": st.column_config.TextColumn("Nome do Conjunto", required=True),
        "Tipo": st.column_config.SelectboxColumn(
            "Tipo (R/C)", options=["R", "C"], required=True
        ),
        "Completo": st.column_config.TextColumn(
            "Completo?",
            help="Indica se todas as partes deste conjunto já foram adquiridas.",
            disabled=True,
        ),
    }

    for key, label in EQUIPMENT_TYPES.items():
        column_config[key] = st.column_config.CheckboxColumn(label)

    return column_config

st.markdown(
    "Edite o **nome**, o **tipo (R/C)** e ative ou desative se uma peça de equipamento pertence ou não a múltiplos conjuntos de uma só vez."
)

sets = load_equipment_sets()

if not sets:
    st.warning("Nenhum conjunto cadastrado.", icon="👻")
else:
    flat_data = build_bulk_edit_rows(sets, list(EQUIPMENT_TYPES.keys()))
    column_config = _build_column_config()

    with st.form("bulk_edit_form"):
        edited_data = st.data_editor(
            flat_data,
            column_config=column_config,
            use_container_width=True,
            num_rows="fixed",
            hide_index=True,
        )

        st.divider()
        submit = st.form_submit_button(
            "💾 Salvar Alterações em Massa", type="primary", use_container_width=True
        )

        if submit:
            bulk_update_from_dataframe(edited_data)
            st.success("✅ Conjuntos atualizados com sucesso!")
            st.rerun()
