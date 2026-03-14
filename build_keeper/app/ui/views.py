import streamlit as st
import unicodedata
from core.equipment_catalog import EQUIPMENT_TYPES
from core.equipment_manager import (
    load_equipment_sets,
    add_equipment_set,
    update_equipment_set,
    delete_equipment_set,
    clone_equipment_set,
    update_equipment_acquisition,
    prepare_set_for_display,
)


def _normalize_search_text(value):
    normalized = unicodedata.normalize("NFKD", str(value or ""))
    return "".join(char for char in normalized if not unicodedata.combining(char)).lower()


def _get_searchable_text(set_data):
    custom_names = []
    for item_data in set_data.get("equipment", {}).values():
        if item_data.get("has_in_set"):
            custom_name = item_data.get("custom_name", "").strip()
            if custom_name:
                custom_names.append(custom_name)

    return _normalize_search_text(" ".join([set_data.get("name", ""), *custom_names]))


def _render_equipment_inputs(form_prefix, equipment_data=None):
    equipment_data = equipment_data or {}
    equipment_flags = {}
    custom_names = {}

    for key, base_label in EQUIPMENT_TYPES.items():
        item_data = equipment_data.get(key, {})
        has_in_set = item_data.get("has_in_set", True if not equipment_data else False)
        custom_name_value = item_data.get("custom_name", "")

        cols = st.columns([1, 2], vertical_alignment="center")
        with cols[0]:
            is_selected = st.checkbox(
                base_label,
                value=has_in_set,
                key=f"{form_prefix}_{key}_check",
            )
            equipment_flags[key] = is_selected
        with cols[1]:
            custom_name = st.text_input(
                "Nome Específico",
                value=custom_name_value,
                key=f"{form_prefix}_{key}_name",
                disabled=not is_selected,
                label_visibility="collapsed",
                placeholder=f"Nome do {base_label.split(' ')[1]}...",
            )
            custom_names[key] = custom_name.strip()

    return equipment_flags, custom_names


def _get_filtered_sets(sets, search_term):
    normalized_search_term = _normalize_search_text(search_term)
    filtered_sets = []

    for set_data in sets:
        prepared_set = prepare_set_for_display(set_data)
        if normalized_search_term and normalized_search_term not in _get_searchable_text(
            prepared_set
        ):
            continue
        filtered_sets.append(prepared_set)

    filtered_sets.sort(key=lambda set_data: set_data["name"].lower())
    return filtered_sets


def _split_sets_by_completion(sets):
    complete_sets = []
    incomplete_sets = []

    for set_data in sets:
        if set_data["_is_complete"]:
            complete_sets.append(set_data)
        else:
            incomplete_sets.append(set_data)

    return incomplete_sets, complete_sets


def render_registration_screen():
    st.header("📋 Novo Conjunto")
    st.markdown(
        "Crie um novo conjunto, selecione as partes e defina nomes personalizados para ter controle total do seu inventário."
    )

    with st.container(border=True):
        with st.form("registration_form"):
            set_name = st.text_input(
                "NOME DO CONJUNTO", placeholder="Ex: Armadura de Batalha Sagrada"
            )
            set_type = st.radio("TIPO", options=["R", "C"], horizontal=True)

            st.divider()
            st.subheader("🧩 Peças do Conjunto")
            st.caption(
                "Selecione quais itens formam este conjunto e o nome específico de cada um deles (opcional)."
            )

            equipment_flags, custom_names = _render_equipment_inputs("new")

            st.divider()
            submitted = st.form_submit_button(
                "Criar Conjunto", type="primary", use_container_width=True
            )

            if submitted:
                if not set_name.strip():
                    st.error("⚠️ Por favor, insira um nome para o conjunto.")
                else:
                    add_equipment_set(set_name, set_type, equipment_flags, custom_names)
                    st.success(f"✅ Conjunto '{set_name}' salvo com sucesso!")


def render_edit_screen(set_data):
    st.header(f"✏️ Editar: {set_data['name']}")

    with st.container(border=True):
        with st.form(f"edit_form_{set_data['id']}"):
            new_set_name = st.text_input("NOME DO CONJUNTO", value=set_data["name"])

            current_type_idx = 0 if set_data.get("type", "R") == "R" else 1
            set_type = st.radio(
                "TIPO", options=["R", "C"], horizontal=True, index=current_type_idx
            )

            st.divider()
            st.subheader("🧩 Peças do Conjunto")

            equipment_flags, custom_names = _render_equipment_inputs(
                f"edit_{set_data['id']}",
                equipment_data=set_data["equipment"],
            )

            st.divider()
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                submitted = st.form_submit_button(
                    "Salvar Alterações", type="primary", use_container_width=True
                )
            with col2:
                canceled = st.form_submit_button("Cancelar", use_container_width=True)
            with col3:
                deleted = st.form_submit_button("🗑️ Excluir", use_container_width=True)

            if submitted:
                if not new_set_name.strip():
                    st.error("⚠️ O nome não pode ser vazio.")
                else:
                    update_equipment_set(
                        set_data["id"],
                        new_set_name,
                        set_type,
                        equipment_flags,
                        custom_names,
                    )
                    st.session_state.edit_mode_id = None
                    st.success("✅ Conjunto atualizado!")
                    st.rerun()

            if canceled:
                st.session_state.edit_mode_id = None
                st.rerun()

            if deleted:
                delete_equipment_set(set_data["id"])
                st.session_state.edit_mode_id = None
                st.success("🗑️ Conjunto removido!")
                st.rerun()


def _render_single_set(s):
    items_in_set = s["_items_in_set"]
    total_items = s["_total_items"]
    acquired_items = s["_acquired_items"]
    is_complete = s["_is_complete"]

    progress_val = (acquired_items / total_items) if total_items > 0 else 0

    expander_title = f"{'🏆 ' if is_complete else '🛡️ '}{s['name']}"

    with st.expander(expander_title, expanded=False):
        if is_complete:
            st.markdown(
                "<div class='completed-badge'>Conjunto Completo! 🎉</div>",
                unsafe_allow_html=True,
            )

        if total_items > 0:
            st.progress(
                progress_val,
                text=f"Progresso de Coleta: {acquired_items}/{total_items} ({int(progress_val * 100)}%)",
            )
            st.divider()

        if not items_in_set:
            st.write(
                "Cuidado: Este conjunto **não possui peças** configuradas. Edite para adicionar partes."
            )
        else:
            for key, data in items_in_set.items():
                base_label = EQUIPMENT_TYPES.get(key, key)
                custom_name = data.get("custom_name", "").strip()

                display_label = (
                    f"**{custom_name}** ({base_label})"
                    if custom_name
                    else f"{base_label}"
                )

                cb_key = f"cb_{s['id']}_{key}"
                current_status = data.get("acquired", False)
                new_status = st.checkbox(
                    display_label, value=current_status, key=cb_key
                )

                if new_status != current_status:
                    update_equipment_acquisition(s["id"], key, new_status)
                    st.rerun()

        st.divider()
        col1, col2 = st.columns([1, 1], gap="medium")
        with col1:
            if st.button(
                "💾 Clonar",
                key=f"btn_clone_{s['id']}",
                use_container_width=True,
            ):
                if clone_equipment_set(s["id"]):
                    st.success("Conjunto clonado com sucesso!")
                    st.rerun()
        with col2:
            if st.button(
                "✏️ Editar",
                key=f"btn_edit_{s['id']}",
                use_container_width=True,
            ):
                st.session_state.edit_mode_id = s["id"]
                st.rerun()


def render_checklist_screen():
    if "edit_mode_id" not in st.session_state:
        st.session_state.edit_mode_id = None

    sets = load_equipment_sets()

    if st.session_state.edit_mode_id:
        target_set = next(
            (s for s in sets if s["id"] == st.session_state.edit_mode_id), None
        )
        if target_set:
            render_edit_screen(target_set)
            return
        else:
            st.session_state.edit_mode_id = None

    st.header("🎯 Tracking de Equipamentos")
    st.markdown("Acompanhe o seu progresso na aquisição das peças de cada conjunto.")

    if not sets:
        st.warning("Nenhum conjunto encontrado.", icon="👻")
        st.info(
            "Utilize a navegação lateral para ir à aba 'Cadastro de Conjunto' e criar o seu primeiro set de equipamentos."
        )
        return

    search_term = st.text_input(
        "Buscar builds",
        placeholder="Ex: cosmo, sentinela ou viseira",
    ).strip()
    filtered_sets = _get_filtered_sets(sets, search_term)
    incomplete_sets, complete_sets = _split_sets_by_completion(filtered_sets)

    def render_sets_in_columns(subset):
        if not subset:
            st.info("Nenhum conjunto nesta categoria.")
            return

        col_r, col_c = st.columns(2)
        for s in subset:
            if s.get("type", "R") == "R":
                with col_r:
                    _render_single_set(s)
            else:
                with col_c:
                    _render_single_set(s)

    if search_term:
        st.caption(
            f"{len(filtered_sets)} build(s) encontrado(s) para '{search_term}'."
        )

    if not filtered_sets:
        st.info("Nenhum build encontrado com esse termo de busca.", icon="🔎")
        return

    st.subheader("🚧 Conjuntos Incompletos")
    render_sets_in_columns(incomplete_sets)

    st.divider()

    st.subheader("🏆 Conjuntos Completos")
    render_sets_in_columns(complete_sets)
