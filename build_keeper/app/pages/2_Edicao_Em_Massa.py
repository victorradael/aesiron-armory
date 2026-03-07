import streamlit as st
from core.settings import Settings
from core.logger import get_logger
from core.equipment_manager import load_equipment_sets, bulk_update_from_dataframe
from ui.views import EQUIPMENT_TYPES

settings = Settings()
logger = get_logger(__name__)

app_name = settings.app_name
st.set_page_config(page_title=f"Edição em Massa - {app_name}", layout="wide")
st.title("📝 Edição em Massa")

logger.info("Renderizando tela: Edição em Massa")

st.markdown(
    "Edite o **nome**, o **tipo (R/C)** e ative ou desative se uma peça de equipamento pertence ou não a múltiplos conjuntos de uma só vez."
)

sets = load_equipment_sets()

if not sets:
    st.warning("Nenhum conjunto cadastrado.", icon="👻")
else:
    flat_data = []
    for s in sets:
        # Calculate progress
        items_in_set = {
            k: v for k, v in s["equipment"].items() if v.get("has_in_set", False)
        }
        total_items = len(items_in_set)
        acquired_items = sum(
            1 for data in items_in_set.values() if data.get("acquired", False)
        )
        is_complete = total_items > 0 and acquired_items == total_items

        row = {
            "id": s["id"],
            "Nome": s["name"],
            "Tipo": s.get("type", "R"),
            "Completo": "✅ Sim" if is_complete else "❌ Não",
        }
        for key, label in EQUIPMENT_TYPES.items():
            row[key] = s["equipment"].get(key, {}).get("has_in_set", False)
        flat_data.append(row)

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
