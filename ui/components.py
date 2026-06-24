import streamlit as st

def format_category(category: str | None) -> str:
    if not category:
        return "Unknown"

    return (
        str(category)
        .replace("_", " ")
        .strip()
        .title()
    )

def render_page_header(
    title: str,
    subtitle: str,
    icon: str = "🔍",
) -> None:
    st.markdown(
        f"""
        <div class="page-header">
            <h1>{icon} {title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_feature_card(
    icon: str,
    title: str,
    description: str,
) -> None:
    st.markdown(
        f"""
        <div class="feature-card">
            <div class="feature-icon">{icon}</div>
            <h3>{title}</h3>
            <p>{description}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_confidence_chip(similarity: float) -> None:
    if similarity >= 0.80:
        label = "High-confidence candidate"
        css_class = "chip-high"
        icon = ""
    elif similarity >= 0.60:
        label = "Moderate-confidence candidate"
        css_class = "chip-medium"
        icon = ""
    else:
        label = "Low-confidence candidate"
        css_class = "chip-low"
        icon = ""

    st.markdown(
        f"""
        <span class="status-chip {css_class}">
            {label}
        </span>
        """,
        unsafe_allow_html=True,
    )

def show_system_information() -> None:
    with st.expander("Technical System Information", expanded=False):
        col1, col2 = st.columns(2)

        with col1:
            st.write("**Frontend:** Streamlit")
            st.write("**Database:** SQLite")
            st.write("**Image feature extractor:** MobileNetV2")
            st.write("**Text processing:** TF-IDF")

        with col2:
            st.write("**Text classifier:** Multinomial Naive Bayes")
            st.write("**Attribute comparison:** Fuzzy rules")
            st.write("**Final classifiers:** KNN, Decision Tree, Random Forest")
            st.write("**Human validation:** Confirm / Reject workflow")

def go_to(page_name: str) -> None:
    st.session_state["current_page"] = page_name
    st.rerun()

def render_topbar(show_back: bool = False) -> None:
    left, middle, right = st.columns(
        [1, 1, 1],
        gap="large",
        vertical_alignment="center",
    )

    with left:
        st.markdown(
            """
            <div class="topbar-left">
                <span class="brand-mark">M</span>
                <span class="topbar-brand-text">MatchAI</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with middle:
        st.markdown(
            """
            <div class="topbar-center">
                <span class="live-badge">
                    <span class="live-dot"></span>
                    System online
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        if show_back:
            if st.button(
                "Back to dashboard",
                key=f"back_{st.session_state.get('current_page', 'page')}",
                type="primary",
                use_container_width=True,
            ):
                go_to("dashboard")
        else:
            st.markdown(
                '<div class="topbar-right-spacer"></div>',
                unsafe_allow_html=True,
            )


def render_action_card(
    icon: str,
    title: str,
    description: str,
    button_label: str,
    target_page: str,
    key: str,
    primary: bool = False,
    icon_class: str = "icon-report",
) -> None:
    del button_label
    del icon_class

    label = (
        f"`{icon}`\n\n"
        f"**{title}**\n\n"
        f"{description}"
    )

    if st.button(
        label,
        key=key,
        type="primary" if primary else "secondary",
        use_container_width=True,
    ):
        go_to(target_page)
