import streamlit as st

from database.database_manager import initialize_database
from ui.pages import (
    show_command_center,
    show_match_history_page,
    show_matching_page,
    show_model_performance_page,
    show_report_form,
    show_reports_page,
)
from ui.styles import apply_custom_style


st.set_page_config(
    page_title="MatchAI",
    page_icon="M",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def main() -> None:
    initialize_database()
    apply_custom_style()

    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "dashboard"

    page = st.session_state["current_page"]

    if page == "dashboard":
        show_command_center()
        return

    from ui.components import render_topbar

    render_topbar(show_back=True)

    if page == "report_lost":
        show_report_form("lost")
    elif page == "report_found":
        show_report_form("found")
    elif page == "find_matches":
        show_matching_page()
    elif page == "reports":
        show_reports_page()
    elif page == "history":
        show_match_history_page()
    elif page == "analytics":
        show_model_performance_page()
    else:
        st.session_state["current_page"] = "dashboard"
        st.rerun()


if __name__ == "__main__":
    main()
