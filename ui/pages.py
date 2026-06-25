from datetime import date
from pathlib import Path

import pandas as pd
import streamlit as st
from st_keyup import st_keyup
from pathlib import Path

print("STREAMLIT PAGES FILE:", Path(__file__).resolve())


from ai_models.cnn_features import extract_and_save_features
from ai_models.final_matcher import rank_matches
from config import ITEM_CATEGORIES
from database.database_manager import (
    add_match,
    add_report,
    get_all_reports,
    get_category_statistics,
    get_dashboard_statistics,
    get_existing_match,
    get_match_history,
    get_match_score_statistics,
    get_opposite_reports,
    get_report_by_id,
    get_report_status_statistics,
    get_report_type_statistics,
    process_match_decision,
    update_report_feature_path,
)
from database.image_manager import save_uploaded_image
from services.extraction_service import (
    extract_smart_report_fields,
    reset_smart_report_state,
)
from ui.components import (
    format_category,
    render_action_card,
    render_confidence_chip,
    render_page_header,
    render_topbar,
)


BASE_DIR = Path(__file__).resolve().parents[1]
CHARTS_DIR = BASE_DIR / "outputs" / "charts"

def format_category(category: str | None) -> str:
    if not category:
        return "Unknown"

    return str(category).replace(
        "_",
        " ",
    ).strip().title()


def show_report_form(report_type: str) -> None:
    is_lost = report_type == "lost"
    prefix = f"smart_{report_type}"

    if is_lost:
        eyebrow = "Lost-item recovery"
        title = "Report an Item You Lost"
        subtitle = (
            "Tell MatchAI what disappeared, where you last had it, "
            "and the details that make it recognisable."
        )
        hero_class = "report-hero-lost"
        eyebrow_class = "report-eyebrow-lost"
        description_label = "Describe the lost item"
        description_placeholder = (
            "Example: I lost a black Adidas backpack with a silver zip, "
            "a red keychain and a scratch near the front pocket."
        )
        image_label = "Upload a photo of the item"
        location_label = "Last known location"
        date_label = "Date lost"
        guidance_class = "lost-guidance"
        guidance_text = (
            "Include unique marks, contents, scratches, accessories or "
            "anything only the owner would recognise."
        )
        save_label = "Save lost-item report"
    else:
        eyebrow = "Found-item registration"
        title = "Report an Item You Found"
        subtitle = (
            "Register the item safely so MatchAI can compare it with "
            "active lost-item reports."
        )
        hero_class = "report-hero-found"
        eyebrow_class = "report-eyebrow-found"
        description_label = "Describe the found item"
        description_placeholder = (
            "Example: I found a black Adidas backpack with a silver zip "
            "and a red keychain near the library entrance."
        )
        image_label = "Upload a clear photo of the found item"
        location_label = "Where the item was found"
        date_label = "Date found"
        guidance_class = "found-guidance"
        guidance_text = (
            "Do not publish private contents or sensitive information. "
            "Record only enough detail for safe matching and verification."
        )
        save_label = "Save found-item report"

    st.markdown(
        f"""
        <div class="report-hero {hero_class}">
            <div class="report-eyebrow {eyebrow_class}">{eyebrow}</div>
            <h1>{title}</h1>
            <p>{subtitle}</p>
            <div class="report-step">
                Live AI extraction · Review details · Save report
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="guidance-box {guidance_class}">
            {guidance_text}
        </div>
        """,
        unsafe_allow_html=True,
    )

    description_col, extraction_col = st.columns([1.15, 1], gap="large")

    with description_col:
        st.markdown(
            """
            <div class="section-panel">
                <div class="section-panel-title">1. Describe and photograph</div>
                <p class="section-panel-copy">
                    MatchAI analyses the description continuously while you type.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        description = st_keyup(
            description_label,
            key=f"{prefix}_description",
            placeholder=description_placeholder,
            debounce=150,
        )

        uploaded_image = st.file_uploader(
            image_label,
            type=["jpg", "jpeg", "png"],
            key=f"{prefix}_image",
        )

    current_description = (description or "").strip()
    last_description_key = f"{prefix}_last_description"
    analysis_key = f"{prefix}_analysis"

    if (
        current_description
        and st.session_state.get(last_description_key)
        != current_description
    ):
        try:
            analysis = extract_smart_report_fields(
                current_description
            )

            st.session_state[analysis_key] = analysis
            st.session_state[f"{prefix}_item_name"] = (
                analysis["item_name"]
            )
            st.session_state[f"{prefix}_category"] = (
                analysis["category"]
            )
            st.session_state[f"{prefix}_category_select"] = (
                analysis["category"]
            )
            st.session_state[f"{prefix}_colour"] = (
                analysis["colour"]
            )
            st.session_state[f"{prefix}_brand"] = (
                analysis["brand"]
            )
            st.session_state[last_description_key] = (
                current_description
            )

        except Exception as error:
            st.session_state[analysis_key] = None
            st.session_state[f"{prefix}_analysis_error"] = str(
                error
            )

    if not current_description:
        st.session_state.pop(analysis_key, None)
        st.session_state.pop(
            f"{prefix}_analysis_error",
            None,
        )
        st.session_state[last_description_key] = ""

    analysis = st.session_state.get(analysis_key)

    with extraction_col:
        st.markdown(
            """
            <div class="section-panel">
                <div class="section-panel-title">2. Review AI extraction</div>
                <p class="section-panel-copy">
                    Correct any value before saving. Human review remains final.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if analysis:
            st.markdown(
                f"""
                <div class="ai-result-card">
                    <div class="ai-result-label">Detected from description</div>
                    <p>
                        Category confidence:
                        <strong>{analysis['confidence']:.1%}</strong><br>
                        Primary colour:
                        <strong>{analysis.get('primary_colour') or 'Not detected'}</strong><br>
                        Accent colours:
                        <strong>{analysis.get('secondary_colours') or 'None detected'}</strong>
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            item_name = st.text_input(
                "Suggested item name",
                key=f"{prefix}_item_name",
            )

            category_value = st.session_state.get(
                f"{prefix}_category_select",
                analysis["category"],
            )

            if category_value not in ITEM_CATEGORIES:
                category_value = ITEM_CATEGORIES[0]
                st.session_state[
                    f"{prefix}_category_select"
                ] = category_value

            category = st.selectbox(
                "Predicted category",
                ITEM_CATEGORIES,
                format_func=format_category,
                key=f"{prefix}_category_select",
            )

            colour = st.text_input(
                "Detected colour",
                key=f"{prefix}_colour",
                placeholder="Not detected",
            )

            brand = st.text_input(
                "Detected brand",
                key=f"{prefix}_brand",
                placeholder="Not detected",
            )

        elif current_description:
            item_name = ""
            category = ITEM_CATEGORIES[0]
            colour = ""
            brand = ""

            extraction_error = st.session_state.get(
                f"{prefix}_analysis_error"
            )

            if extraction_error:
                st.error(
                    "Live extraction could not complete: "
                    f"{extraction_error}"
                )
            else:
                st.info(
                    "MatchAI is processing the description."
                )

        else:
            item_name = ""
            category = ITEM_CATEGORIES[0]
            colour = ""
            brand = ""

            st.info(
                "Start typing to see the extracted item details."
            )

    st.markdown(
        """
        <div class="section-panel">
            <div class="section-panel-title">3. Add report and contact details</div>
            <p class="section-panel-copy">
                These details help narrow candidates and contact the reporter.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    details_col1, details_col2, details_col3 = st.columns(
        [1, 1, 1],
        gap="large",
    )

    with details_col1:
        location = st.text_input(
            location_label,
            key=f"{prefix}_location",
            placeholder=(
                "Example: University Library"
                if is_lost
                else "Example: Library entrance"
            ),
        )

        report_date = st.date_input(
            date_label,
            value=date.today(),
            key=f"{prefix}_date",
        )

    with details_col2:
        contact_name = st.text_input(
            "Contact name",
            key=f"{prefix}_contact_name",
        )

        contact_email = st.text_input(
            "Contact email",
            key=f"{prefix}_contact_email",
        )

    with details_col3:
        contact_phone = st.text_input(
            "Contact phone",
            key=f"{prefix}_contact_phone",
        )

        st.caption(
            "Contact information is stored with the report "
            "and is not used as an AI matching feature."
        )

    st.markdown(
        '<div class="save-report-button">',
        unsafe_allow_html=True,
    )
    submit_clicked = st.button(
        save_label,
        key=f"{prefix}_submit",
        type="primary",
        use_container_width=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    if not submit_clicked:
        return

    errors = []

    if not current_description:
        errors.append("Item description is required.")
    if analysis is None:
        errors.append(
            "MatchAI could not extract the item details. "
            "Check the description and try again."
        )
    if not item_name.strip():
        errors.append(
            "Enter or correct the suggested item name."
        )
    if not location.strip():
        errors.append(f"{location_label} is required.")
    if not contact_name.strip():
        errors.append("Contact name is required.")
    if not contact_email.strip():
        errors.append("Contact email is required.")
    if uploaded_image is None:
        errors.append("An item image is required.")

    if errors:
        for error in errors:
            st.error(error)
        return

    try:
        image_path = save_uploaded_image(
            uploaded_file=uploaded_image,
            report_type=report_type,
        )

        report_id = add_report(
            report_type=report_type,
            item_name=item_name.strip(),
            category=category,
            description=current_description,
            colour=colour.strip(),
            brand=brand.strip(),
            location=location.strip(),
            report_date=str(report_date),
            contact_name=contact_name.strip(),
            contact_email=contact_email.strip(),
            contact_phone=contact_phone.strip(),
            image_path=image_path,
        )

        try:
            feature_path = extract_and_save_features(
                image_path=image_path,
                report_id=report_id,
                report_type=report_type,
            )

            update_report_feature_path(
                report_id=report_id,
                feature_path=feature_path,
            )

        except Exception as feature_error:
            st.warning(
                "The report was saved, but its image feature "
                f"could not be generated: {feature_error}"
            )

        st.success(
            f"{'Lost' if is_lost else 'Found'} report saved successfully. "
            f"Report ID: {report_id}"
        )

        summary_col1, summary_col2 = st.columns([1, 2])

        with summary_col1:
            st.image(
                image_path,
                caption="Submitted item",
                use_container_width=True,
            )

        with summary_col2:
            st.write(f"**Item:** {item_name}")
            st.write(
                f"**Category:** {format_category(category)}"
            )
            st.write(
                f"**Colour:** {colour or 'Not detected'}"
            )
            st.write(
                f"**Brand:** {brand or 'Not detected'}"
            )
            st.write(
                f"**AI category confidence:** "
                f"{analysis['confidence']:.1%}"
            )

    except Exception as error:
        st.error(f"Could not save the report: {error}")

def show_reports_page() -> None:
    render_page_header(
        title="Stored Reports",
        subtitle="Review all lost and found reports currently saved in the system.",
        icon="DATA",
    )

    reports = get_all_reports()

    if not reports:
        st.info("No reports have been submitted yet.")
        return

    dataframe = pd.DataFrame(reports)

    display_columns = [
        "report_id",
        "report_type",
        "item_name",
        "category",
        "colour",
        "brand",
        "location",
        "report_date",
        "status",
        "created_at",
    ]

    available_columns = [
        column
        for column in display_columns
        if column in dataframe.columns
    ]

    st.dataframe(
        dataframe[available_columns],
        use_container_width=True,
        hide_index=True,
    )

    st.subheader("Report Details")

    report_ids = [
        report["report_id"]
        for report in reports
    ]

    selected_report_id = st.selectbox(
        "Select a report",
        report_ids,
    )

    selected_report = next(
        report
        for report in reports
        if report["report_id"] == selected_report_id
    )

    col1, col2 = st.columns([1, 2])

    with col1:
        if selected_report["image_path"]:
            st.image(
                selected_report["image_path"],
                caption=selected_report["item_name"],
                use_container_width=True,
            )

    with col2:
        st.write(
            f"**Type:** {selected_report['report_type'].title()}"
        )
        st.write(
            f"**Category:** {format_category(selected_report['category'])}"
        )
        st.write(
            f"**Description:** {selected_report['description']}"
        )
        st.write(
            f"**Colour:** {selected_report['colour'] or 'Not provided'}"
        )
        st.write(
            f"**Brand:** {selected_report['brand'] or 'Not provided'}"
        )
        st.write(
            f"**Location:** {selected_report['location']}"
        )
        st.write(
            f"**Date:** {selected_report['report_date']}"
        )
        st.write(
            f"**Contact:** {selected_report['contact_name']}"
        )
        st.write(
            f"**Email:** {selected_report['contact_email']}"
        )
        st.write(
            f"**Phone:** {selected_report['contact_phone'] or 'Not provided'}"
        )
        st.write(
            f"**Status:** {selected_report['status'].title()}"
        )

def save_candidate_match(
    source_report: dict,
    candidate: dict,
) -> int:
    if source_report["report_type"] == "lost":
        lost_report_id = source_report["report_id"]
        found_report_id = candidate["report_id"]

    else:
        lost_report_id = candidate["report_id"]
        found_report_id = source_report["report_id"]

    existing_match = get_existing_match(
        lost_report_id=lost_report_id,
        found_report_id=found_report_id,
    )

    if existing_match is not None:
        return int(existing_match["match_id"])

    return add_match(
        lost_report_id=lost_report_id,
        found_report_id=found_report_id,
        image_similarity=candidate["image_similarity"],
        text_similarity=candidate["text_similarity"],
        category_similarity=candidate["category_similarity"],
        colour_similarity=candidate["colour_similarity"],
        brand_similarity=candidate["brand_similarity"],
        location_similarity=candidate["location_similarity"],
        date_similarity=candidate["date_similarity"],
        final_probability=candidate["final_score"],
    )

def show_matching_page() -> None:
    render_page_header(
        title="Find Potential Matches",
        subtitle="Select an active report and let MatchAI rank the best opposite reports.",
        icon="🎯",
    )

    if "match_message" in st.session_state:
        message_type = st.session_state.pop(
            "match_message_type",
            "success",
        )
        message = st.session_state.pop("match_message")

        if message_type == "success":
            st.success(message)
        elif message_type == "warning":
            st.warning(message)
        else:
            st.error(message)

    reports = [
        report
        for report in get_all_reports()
        if report["status"] == "active"
    ]

    if not reports:
        st.info("No active reports are available.")
        return

    report_options = {
        (
            f"ID {report['report_id']} | "
            f"{report['report_type'].title()} | "
            f"{report['item_name']}"
        ): report["report_id"]
        for report in reports
    }

    selected_label = st.selectbox(
        "Select a report to search matches for",
        list(report_options.keys()),
        key="match_source_selector",
    )

    selected_report_id = report_options[selected_label]
    selected_report = get_report_by_id(selected_report_id)

    if selected_report is None:
        st.error("Selected report could not be found.")
        return

    previous_source_id = st.session_state.get(
        "match_source_report_id"
    )

    if previous_source_id != selected_report_id:
        st.session_state["match_source_report_id"] = (
            selected_report_id
        )
        st.session_state.pop("ranked_matches", None)

    st.subheader("Selected Report")
    st.caption(
        "The system will compare this report against "
        "active reports of the opposite type."
    )

    col1, col2 = st.columns([1, 2])

    with col1:
        if selected_report.get("image_path"):
            st.image(
                selected_report["image_path"],
                use_container_width=True,
            )

    with col2:
        st.write(f"**Item:** {selected_report['item_name']}")
        st.write(
            f"**Type:** {selected_report['report_type'].title()}"
        )
        st.write(
            f"**Category:** "
            f"{format_category(selected_report['category'])}"
        )
        st.write(
            f"**Description:** {selected_report['description']}"
        )
        st.write(f"**Location:** {selected_report['location']}")
        st.write(f"**Date:** {selected_report['report_date']}")

    candidates = get_opposite_reports(
        selected_report["report_type"]
    )

    if not candidates:
        st.warning(
            "No active opposite report type is available. "
            "Add both lost and found reports first."
        )
        st.session_state.pop("ranked_matches", None)
        return

    if st.button(
        "Find Matches",
        type="primary",
    ):
        with st.spinner(
            "Analysing images, text and item attributes..."
        ):
            ranked_matches = rank_matches(
                selected_report,
                candidates,
            )

        st.session_state["ranked_matches"] = ranked_matches
        st.session_state["matching_source_report_id"] = (
            selected_report["report_id"]
        )

    ranked_matches = st.session_state.get(
        "ranked_matches",
        [],
    )

    if not ranked_matches:
        st.info(
            "Press Find Matches to calculate "
            "potential matches."
        )
        return

    st.subheader(
        "Potential Matches Ranked by Combined AI Score"
    )

    st.caption(
        "Candidates are ordered from the highest "
        "AI match probability to the lowest."
    )

    for index, candidate in enumerate(
        ranked_matches[:5],
        start=1,
    ):
        similarity = float(candidate["final_score"])

        with st.container(border=True):
            left, right = st.columns([1, 3])

            with left:
                if candidate.get("image_path"):
                    st.image(
                        candidate["image_path"],
                        use_container_width=True,
                    )

            with right:
                st.markdown(
                    f"### #{index} {candidate['item_name']}"
                )

                st.progress(
                    max(0.0, min(1.0, similarity))
                )

                st.write(
                    f"**Overall match score:** "
                    f"{similarity:.1%}"
                )

                render_confidence_chip(similarity)

                st.write(
                    f"**Match strength:** "
                    f"{candidate['match_strength']}"
                )

                st.write(
                    f"**Scoring method:** "
                    f"{candidate['score_method']}"
                )

                st.write(
                    f"**Weighted baseline:** "
                    f"{candidate['weighted_score']:.1%}"
                )

                st.write(
                    f"**Category:** "
                    f"{format_category(candidate['category'])}"
                )

                score_col1, score_col2 = st.columns(2)

                with score_col1:
                    st.write(
                        f"**Image similarity:** "
                        f"{candidate['image_similarity']:.1%}"
                    )
                    st.write(
                        f"**Text similarity:** "
                        f"{candidate['text_similarity']:.1%}"
                    )
                    st.write(
                        f"**Category similarity:** "
                        f"{candidate['category_similarity']:.1%}"
                    )
                    st.write(
                        f"**Colour similarity:** "
                        f"{candidate['colour_similarity']:.1%}"
                    )

                with score_col2:
                    st.write(
                        f"**Brand similarity:** "
                        f"{candidate['brand_similarity']:.1%}"
                    )
                    st.write(
                        f"**Location similarity:** "
                        f"{candidate['location_similarity']:.1%}"
                    )
                    st.write(
                        f"**Date similarity:** "
                        f"{candidate['date_similarity']:.1%}"
                    )

                st.markdown(
                    "**Why this result was recommended:**"
                )

                for reason in candidate["explanations"]:
                    st.write(f"- {reason}")

                st.write(
                    f"**Description:** "
                    f"{candidate['description']}"
                )
                st.write(
                    f"**Location:** {candidate['location']}"
                )
                st.write(
                    f"**Date:** {candidate['report_date']}"
                )

                st.divider()

                decision_col1, decision_col2 = st.columns(2)

                match_key = (
                    f"{selected_report['report_id']}_"
                    f"{candidate['report_id']}"
                )

                with decision_col1:
                    confirm_clicked = st.button(
                        "Confirm Match",
                        key=f"confirm_{match_key}",
                        type="primary",
                        use_container_width=True,
                    )

                with decision_col2:
                    reject_clicked = st.button(
                        "Reject Match",
                        key=f"reject_{match_key}",
                        use_container_width=True,
                    )

                if confirm_clicked:
                    try:
                        match_id = save_candidate_match(
                            selected_report,
                            candidate,
                        )

                        process_match_decision(
                            match_id=match_id,
                            decision="confirmed",
                            notes=(
                                "Confirmed by user through "
                                "the MatchAI interface."
                            ),
                        )

                        st.session_state["match_message"] = (
                            f"Match ID {match_id} was confirmed "
                            "successfully. Both reports are now "
                            "marked as matched. Open Match History "
                            "to view the decision."
                        )
                        st.session_state[
                            "match_message_type"
                        ] = "success"
                        st.session_state.pop(
                            "ranked_matches",
                            None,
                        )
                        st.rerun()

                    except Exception as error:
                        st.error(
                            f"Could not confirm match: {error}"
                        )

                if reject_clicked:
                    try:
                        match_id = save_candidate_match(
                            selected_report,
                            candidate,
                        )

                        process_match_decision(
                            match_id=match_id,
                            decision="rejected",
                            notes=(
                                "Rejected by user through "
                                "the MatchAI interface."
                            ),
                        )

                        st.session_state["match_message"] = (
                            f"Match ID {match_id} was rejected. "
                            "The reports remain active."
                        )
                        st.session_state[
                            "match_message_type"
                        ] = "warning"
                        st.session_state.pop(
                            "ranked_matches",
                            None,
                        )
                        st.rerun()

                    except Exception as error:
                        st.error(
                            f"Could not reject match: {error}"
                        )

def show_match_history_page() -> None:
    render_page_header(
        title="Match Decision History",
        subtitle="View confirmed, rejected and pending match decisions saved by users.",
    )

    try:
        matches = get_match_history()
    except Exception as error:
        st.error(
            f"Could not load match history: {error}"
        )
        return

    if not matches:
        st.info(
            "No match decisions have been saved yet."
        )
        return

    status_filter = st.selectbox(
        "Filter by status",
        [
            "All",
            "Confirmed",
            "Rejected",
            "Pending",
        ],
    )

    if status_filter == "All":
        filtered_matches = matches
    else:
        filtered_matches = [
            match
            for match in matches
            if (
                match["match_status"].lower()
                == status_filter.lower()
            )
        ]

    if not filtered_matches:
        st.info(
            "No match records exist for this status."
        )
        return

    for match in filtered_matches:
        with st.container(border=True):
            st.markdown(
                f"### Match ID {match['match_id']}"
            )

            status = match["match_status"].title()

            if match["match_status"] == "confirmed":
                st.success(f"Status: {status}")
            elif match["match_status"] == "rejected":
                st.error(f"Status: {status}")
            else:
                st.warning(f"Status: {status}")

            lost_col, found_col = st.columns(2)

            with lost_col:
                st.markdown("#### Lost Item")

                if match.get("lost_image_path"):
                    st.image(
                        match["lost_image_path"],
                        use_container_width=True,
                    )

                st.write(
                    f"**Item:** {match['lost_item_name']}"
                )
                st.write(
                    f"**Description:** "
                    f"{match['lost_description']}"
                )
                st.write(
                    f"**Location:** "
                    f"{match['lost_location']}"
                )
                st.write(
                    f"**Date:** {match['lost_date']}"
                )

            with found_col:
                st.markdown("#### Found Item")

                if match.get("found_image_path"):
                    st.image(
                        match["found_image_path"],
                        use_container_width=True,
                    )

                st.write(
                    f"**Item:** {match['found_item_name']}"
                )
                st.write(
                    f"**Description:** "
                    f"{match['found_description']}"
                )
                st.write(
                    f"**Location:** "
                    f"{match['found_location']}"
                )
                st.write(
                    f"**Date:** {match['found_date']}"
                )

            st.write(
                f"**Final probability:** "
                f"{match['final_probability']:.1%}"
            )

            st.write(
                f"**Decision saved:** "
                f"{match['created_at']}"
            )

def find_first_existing_file(
    filenames: list[str],
) -> Path | None:
    for filename in filenames:
        file_path = CHARTS_DIR / filename

        if file_path.exists():
            return file_path

    return None

def show_model_performance_section() -> None:
    st.header("Model Performance")

    st.write(
        "This section displays evaluation results "
        "for KNN, Decision Tree and Random Forest."
    )

    comparison_csv = find_first_existing_file(
        [
            "model_comparison.csv",
            "model_metrics.csv",
            "final_model_comparison.csv",
            "classifier_comparison.csv",
        ]
    )

    if comparison_csv is not None:
        try:
            results_dataframe = pd.read_csv(
                comparison_csv
            )

            st.subheader("Algorithm Comparison")

            st.dataframe(
                results_dataframe,
                use_container_width=True,
                hide_index=True,
            )

            numeric_columns = (
                results_dataframe.select_dtypes(
                    include="number"
                ).columns.tolist()
            )

            model_column = next(
                (
                    column
                    for column in [
                        "model",
                        "Model",
                        "algorithm",
                        "Algorithm",
                    ]
                    if column
                    in results_dataframe.columns
                ),
                None,
            )

            if (
                model_column is not None
                and numeric_columns
            ):
                chart_dataframe = (
                    results_dataframe.set_index(
                        model_column
                    )
                )

                st.bar_chart(
                    chart_dataframe[
                        numeric_columns
                    ],
                    use_container_width=True,
                )

        except Exception as error:
            st.warning(
                "The model comparison file could "
                f"not be displayed: {error}"
            )

    else:
        st.info(
            "No model comparison CSV was found. "
            "Run the final matcher training script."
        )

    comparison_chart = find_first_existing_file(
        [
            "model_comparison.png",
            "model_performance_comparison.png",
            "classifier_comparison.png",
            "final_model_comparison.png",
        ]
    )

    if comparison_chart is not None:
        st.subheader("Model Comparison Chart")

        st.image(
            str(comparison_chart),
            use_container_width=True,
        )

    st.subheader("Confusion Matrices")

    confusion_matrix_files = {
        "K-Nearest Neighbours": [
            "knn_confusion_matrix.png",
            "k_nearest_neighbors_confusion_matrix.png",
        ],
        "Decision Tree": [
            "decision_tree_confusion_matrix.png",
            "decisiontree_confusion_matrix.png",
        ],
        "Random Forest": [
            "random_forest_confusion_matrix.png",
            "randomforest_confusion_matrix.png",
        ],
    }

    matrices_found = False

    for model_name, filenames in (
        confusion_matrix_files.items()
    ):
        matrix_path = find_first_existing_file(
            filenames
        )

        if matrix_path is not None:
            matrices_found = True

            with st.expander(
                model_name,
                expanded=True,
            ):
                st.image(
                    str(matrix_path),
                    caption=(
                        f"{model_name} Confusion Matrix"
                    ),
                    use_container_width=True,
                )

    if not matrices_found:
        st.info(
            "No confusion-matrix images were found "
            "inside outputs/charts."
        )

    st.subheader("Metric Interpretation")

    st.write(
        "**Accuracy:** Percentage of all predictions "
        "classified correctly."
    )

    st.write(
        "**Precision:** Percentage of predicted matches "
        "that were genuine matches."
    )

    st.write(
        "**Recall:** Percentage of genuine matches "
        "successfully detected."
    )

    st.write(
        "**F1-score:** Balance between precision "
        "and recall."
    )

    st.write(
        "**False positive:** A wrong item was "
        "classified as a match."
    )

    st.write(
        "**False negative:** A real match was missed."
    )

    st.warning(
        "False positives are important because they "
        "may connect an item to the wrong report."
    )

def show_dashboard_page() -> None:
    render_page_header(
        title="MatchAI Dashboard",
        subtitle="Monitor reports, decisions, scores and model-evaluation evidence.",
        icon="ML",
    )

    try:
        statistics = get_dashboard_statistics()
        category_statistics = get_category_statistics()
        status_statistics = get_report_status_statistics()
        type_statistics = get_report_type_statistics()
        match_scores = get_match_score_statistics()

    except Exception as error:
        st.error(
            f"Could not load dashboard data: {error}"
        )
        return

    st.subheader("System Overview")

    metric_col1, metric_col2, metric_col3, metric_col4 = (
        st.columns(4)
    )

    with metric_col1:
        st.metric(
            "Total Reports",
            statistics["total_reports"],
        )

    with metric_col2:
        st.metric(
            "Lost Reports",
            statistics["total_lost"],
        )

    with metric_col3:
        st.metric(
            "Found Reports",
            statistics["total_found"],
        )

    with metric_col4:
        st.metric(
            "Active Reports",
            statistics["active_reports"],
        )

    metric_col5, metric_col6, metric_col7, metric_col8 = (
        st.columns(4)
    )

    with metric_col5:
        st.metric(
            "Matched Reports",
            statistics["matched_reports"],
        )

    with metric_col6:
        st.metric(
            "Confirmed Matches",
            statistics["confirmed_matches"],
        )

    with metric_col7:
        st.metric(
            "Rejected Matches",
            statistics["rejected_matches"],
        )

    with metric_col8:
        st.metric(
            "Pending Matches",
            statistics["pending_matches"],
        )

    st.divider()

    performance_col1, performance_col2 = st.columns(2)

    with performance_col1:
        st.metric(
            "Confirmation Rate",
            f"{statistics['confirmation_rate']:.1%}",
        )

    with performance_col2:
        st.metric(
            "Average AI Match Probability",
            f"{statistics['average_probability']:.1%}",
        )

    st.divider()

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.subheader("Reports by Category")

        if category_statistics:
            category_dataframe = pd.DataFrame(
                category_statistics
            )

            category_dataframe["category"] = (
                category_dataframe[
                    "category"
                ].apply(format_category)
            )

            category_chart = (
                category_dataframe.set_index(
                    "category"
                )
            )

            st.bar_chart(
                category_chart["report_count"],
                use_container_width=True,
            )

            st.dataframe(
                category_dataframe,
                use_container_width=True,
                hide_index=True,
            )

        else:
            st.info(
                "No category data is available."
            )

    with chart_col2:
        st.subheader("Reports by Status")

        if status_statistics:
            status_dataframe = pd.DataFrame(
                status_statistics
            )

            status_dataframe["status"] = (
                status_dataframe[
                    "status"
                ].str.title()
            )

            status_chart = (
                status_dataframe.set_index(
                    "status"
                )
            )

            st.bar_chart(
                status_chart["report_count"],
                use_container_width=True,
            )

            st.dataframe(
                status_dataframe,
                use_container_width=True,
                hide_index=True,
            )

        else:
            st.info(
                "No report-status data is available."
            )

    st.divider()

    st.subheader("Lost and Found Distribution")

    if type_statistics:
        type_dataframe = pd.DataFrame(type_statistics)

        type_dataframe["report_type"] = (
            type_dataframe[
                "report_type"
            ].str.title()
        )

        type_chart = (
            type_dataframe.set_index(
                "report_type"
            )
        )

        st.bar_chart(
            type_chart["report_count"],
            use_container_width=True,
        )

        st.dataframe(
            type_dataframe,
            use_container_width=True,
            hide_index=True,
        )

    else:
        st.info(
            "No report-type data is available."
        )

    st.divider()

    st.subheader("AI Match Decision Records")

    if match_scores:
        match_dataframe = pd.DataFrame(match_scores)

        match_dataframe[
            "final_probability_percentage"
        ] = (
            match_dataframe[
                "final_probability"
            ] * 100
        ).round(1)

        display_match_dataframe = (
            match_dataframe[
                [
                    "match_id",
                    "lost_report_id",
                    "found_report_id",
                    "final_probability_percentage",
                    "match_status",
                    "created_at",
                ]
            ].copy()
        )

        display_match_dataframe = (
            display_match_dataframe.rename(
                columns={
                    "match_id": "Match ID",
                    "lost_report_id": "Lost Report ID",
                    "found_report_id": "Found Report ID",
                    "final_probability_percentage": (
                        "AI Probability (%)"
                    ),
                    "match_status": "Decision",
                    "created_at": "Created At",
                }
            )
        )

        display_match_dataframe[
            "Decision"
        ] = display_match_dataframe[
            "Decision"
        ].str.title()

        st.dataframe(
            display_match_dataframe,
            use_container_width=True,
            hide_index=True,
        )

        score_chart = match_dataframe[
            [
                "match_id",
                "final_probability",
            ]
        ].copy()

        score_chart["match_id"] = (
            score_chart[
                "match_id"
            ].astype(str)
        )

        score_chart = score_chart.set_index(
            "match_id"
        )

        st.bar_chart(
            score_chart["final_probability"],
            use_container_width=True,
        )

    else:
        st.info(
            "No match-decision records are available."
        )

    st.divider()

    show_model_performance_section()

def show_command_center() -> None:
    render_topbar(show_back=False)

    st.markdown(
        """
        <style>
        /*
        Dashboard cards:
        - preserve the white-card design
        - blue accent for core actions
        - teal accent for management actions
        - keep all text inside each card
        */
        div[data-testid="stButton"] > button[
            data-testid="baseButton-primary"
        ],
        div[data-testid="stButton"] > button[
            data-testid="baseButton-secondary"
        ] {
            width: 100% !important;
            min-height: 215px !important;
            height: 215px !important;

            padding: 1.3rem 1.4rem !important;
            border-radius: 24px !important;
            border: 1px solid #d8e1ed !important;

            text-align: left !important;
            justify-content: flex-start !important;
            align-items: flex-start !important;

            white-space: normal !important;
            overflow: hidden !important;

            box-shadow:
                0 14px 32px
                rgba(15, 23, 42, 0.09) !important;

            transition:
                transform 0.2s ease,
                box-shadow 0.2s ease,
                border-color 0.2s ease !important;
        }

        /* Core-action cards. */
        div[data-testid="stButton"] > button[
            data-testid="baseButton-primary"
        ] {
            background:
                radial-gradient(
                    circle at 92% 8%,
                    rgba(34, 211, 238, 0.16),
                    transparent 34%
                ),
                linear-gradient(
                    145deg,
                    #ffffff,
                    #eef7ff
                ) !important;

            color: #1e293b !important;
            border-top: 4px solid #2563eb !important;
        }

        /* Management cards. */
        div[data-testid="stButton"] > button[
            data-testid="baseButton-secondary"
        ] {
            background:
                radial-gradient(
                    circle at 92% 8%,
                    rgba(99, 102, 241, 0.10),
                    transparent 34%
                ),
                #ffffff !important;

            color: #1e293b !important;
            border-top: 4px solid #14b8a6 !important;
        }

        div[data-testid="stButton"] > button:hover {
            transform: translateY(-4px) !important;
            border-color: #60a5fa !important;

            box-shadow:
                0 22px 44px
                rgba(15, 23, 42, 0.15) !important;
        }

        /* All card text remains inside the card. */
        div[data-testid="stButton"] > button p {
            width: 100% !important;
            max-width: 100% !important;
            margin: 0 !important;

            color: #64748b !important;
            text-align: left !important;

            font-size: 0.98rem !important;
            line-height: 1.48 !important;

            white-space: normal !important;
            overflow-wrap: anywhere !important;
            word-break: normal !important;
        }

        /* Card title. */
        div[data-testid="stButton"] > button strong {
            display: block !important;

            margin:
                0.7rem
                0
                0.45rem
                0 !important;

            color: #1e293b !important;

            font-size: 1.15rem !important;
            line-height: 1.28 !important;
            font-weight: 850 !important;

            white-space: normal !important;
            overflow-wrap: anywhere !important;
        }

        /* LOST, FOUND, AI, DATA, LOG and ML labels. */
        div[data-testid="stButton"] > button code {
            display: inline-block !important;

            padding:
                0.36rem
                0.62rem !important;

            border-radius: 10px !important;

            background: #e5efff !important;
            color: #1d4ed8 !important;

            font-family: inherit !important;
            font-size: 0.73rem !important;
            font-weight: 900 !important;
            letter-spacing: 0.08em !important;
        }

        @media (max-width: 900px) {
            div[data-testid="stButton"] > button[
                data-testid="baseButton-primary"
            ],
            div[data-testid="stButton"] > button[
                data-testid="baseButton-secondary"
            ] {
                min-height: 205px !important;
                height: auto !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="command-shell">
            <div class="command-hero">
                <div class="hero-kicker">AI-powered recovery platform</div>
                <h1>Find what was lost.<br>Return what was found.</h1>
                <p>
                    Report an item, run intelligent matching, and confirm the right owner —
                    all from one focused command center.
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    try:
        stats = get_dashboard_statistics()
    except Exception:
        stats = {
            "active_reports": 0,
            "matched_reports": 0,
            "confirmed_matches": 0,
            "total_reports": 0,
        }

    metric_cols = st.columns(4)
    metric_values = [
        ("Active reports", stats.get("active_reports", 0)),
        ("Resolved reports", stats.get("matched_reports", 0)),
        ("Confirmed matches", stats.get("confirmed_matches", 0)),
        ("Total reports", stats.get("total_reports", 0)),
    ]

    for column, (label, value) in zip(metric_cols, metric_values):
        with column:
            st.metric(label, value)

    st.markdown('<div class="section-label">Core actions</div>', unsafe_allow_html=True)

    action_row_1 = st.columns(3)
    with action_row_1[0]:
        render_action_card(
            "LOST",
            "Report a lost item",
            "Upload a photo and describe what you lost.",
            "Open lost-item form",
            "report_lost",
            "open_lost",
            primary=True,
            icon_class="icon-lost",
        )
    with action_row_1[1]:
        render_action_card(
            "FOUND",
            "Report a found item",
            "Register a found item for AI comparison.",
            "Open found-item form",
            "report_found",
            "open_found",
            primary=True,
            icon_class="icon-found",
        )
    with action_row_1[2]:
        render_action_card(
            "AI",
            "Find matches",
            "Run multimodal AI matching and review ranked candidates.",
            "Start AI matching",
            "find_matches",
            "open_matching",
            primary=True,
            icon_class="icon-match",
        )

    st.markdown('<div class="section-label">Manage and analyse</div>', unsafe_allow_html=True)

    action_row_2 = st.columns(3)
    with action_row_2[0]:
        render_action_card(
            "DATA",
            "Browse reports",
            "Review saved reports, images and statuses.",
            "Browse reports",
            "reports",
            "open_reports",
            icon_class="icon-report",
        )
    with action_row_2[1]:
        render_action_card(
            "LOG",
            "Match history",
            "Inspect confirmed, rejected and pending match decisions.",
            "View match history",
            "history",
            "open_history",
            icon_class="icon-history",
        )
    with action_row_2[2]:
        render_action_card(
            "ML",
            "Analytics and models",
            "Inspect statistics, model metrics and confusion matrices.",
            "Open analytics",
            "analytics",
            "open_analytics",
            icon_class="icon-analytics",
        )

    st.markdown('<div class="section-label">How it works</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="workflow-strip">
            <div class="workflow-step">
                <div class="workflow-number">STEP 01</div>
                <div class="workflow-title">Submit</div>
                <div class="workflow-copy">Upload a photo and item details.</div>
            </div>
            <div class="workflow-step">
                <div class="workflow-number">STEP 02</div>
                <div class="workflow-title">Analyse</div>
                <div class="workflow-copy">Image, text and metadata are scored.</div>
            </div>
            <div class="workflow-step">
                <div class="workflow-number">STEP 03</div>
                <div class="workflow-title">Rank</div>
                <div class="workflow-copy">The strongest candidates appear first.</div>
            </div>
            <div class="workflow-step">
                <div class="workflow-number">STEP 04</div>
                <div class="workflow-title">Confirm</div>
                <div class="workflow-copy">A human validates the final match.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def show_model_performance_page() -> None:
    render_page_header(
        "Analytics and Model Performance",
        "Monitor system activity and compare the trained matching algorithms.",
    )
    show_dashboard_page()
