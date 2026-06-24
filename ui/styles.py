import streamlit as st


def apply_custom_style() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        :root {
            --matchai-bg: #f3f7fb;
            --matchai-card: #ffffff;
            --matchai-primary: #2563eb;
            --matchai-primary-dark: #1e40af;
            --matchai-accent: #06b6d4;
            --matchai-success: #16a34a;
            --matchai-warning: #f59e0b;
            --matchai-danger: #dc2626;
            --matchai-text: #0f172a;
            --matchai-muted: #64748b;
            --matchai-border: #dbe4f0;
            --matchai-shadow: 0 14px 35px rgba(15, 23, 42, 0.08);
        }

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(37, 99, 235, 0.14), transparent 30%),
                radial-gradient(circle at top right, rgba(6, 182, 212, 0.16), transparent 28%),
                var(--matchai-bg);
        }

        .block-container {
            padding-top: 4.6rem;
            padding-bottom: 2.8rem;
            max-width: 1240px;
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0f172a 0%, #172554 58%, #1e3a8a 100%);
            border-right: 0;
        }

        [data-testid="stSidebar"] * {
            color: #e5eefc !important;
        }

        [data-testid="stSidebar"] .stRadio > label {
            color: #bfdbfe !important;
            font-weight: 700;
            letter-spacing: 0.03em;
            text-transform: uppercase;
            font-size: 0.75rem;
        }

        [data-testid="stSidebar"] [role="radiogroup"] label {
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.10);
            border-radius: 14px;
            margin: 0.28rem 0;
            padding: 0.55rem 0.75rem;
            transition: all 0.18s ease;
        }

        [data-testid="stSidebar"] [role="radiogroup"] label:hover {
            background: rgba(255, 255, 255, 0.16);
            transform: translateX(3px);
        }

        h1, h2, h3 {
            color: var(--matchai-text);
            letter-spacing: -0.025em;
        }

        p, li, label, .stMarkdown {
            color: #334155;
        }

        .app-hero {
            background:
                linear-gradient(135deg, rgba(15, 23, 42, 0.94), rgba(30, 64, 175, 0.94)),
                linear-gradient(45deg, #2563eb, #06b6d4);
            border-radius: 28px;
            padding: 2.5rem 2.2rem;
            color: white;
            box-shadow: var(--matchai-shadow);
            margin-bottom: 1.4rem;
            position: relative;
            overflow: hidden;
        }

        .app-hero::after {
            content: "";
            position: absolute;
            width: 260px;
            height: 260px;
            right: -70px;
            top: -80px;
            background: rgba(255, 255, 255, 0.14);
            border-radius: 999px;
        }

        .app-hero h1 {
            color: white;
            font-size: 3rem;
            line-height: 1.05;
            margin: 0 0 0.75rem 0;
        }

        .app-hero p {
            color: #dbeafe;
            font-size: 1.05rem;
            max-width: 760px;
            margin-bottom: 1.25rem;
        }

        .hero-pill {
            display: inline-block;
            background: rgba(255, 255, 255, 0.14);
            border: 1px solid rgba(255, 255, 255, 0.22);
            border-radius: 999px;
            padding: 0.45rem 0.8rem;
            color: #eff6ff;
            margin-right: 0.45rem;
            margin-bottom: 0.45rem;
            font-size: 0.9rem;
            font-weight: 600;
        }

        .page-header {
            background: rgba(255, 255, 255, 0.86);
            border: 1px solid rgba(219, 228, 240, 0.95);
            border-radius: 22px;
            padding: 1.45rem 1.6rem;
            box-shadow: 0 10px 26px rgba(15, 23, 42, 0.055);
            margin-bottom: 1.2rem;
        }

        .page-header h1 {
            margin: 0;
            font-size: 2.05rem;
        }

        .page-header p {
            color: var(--matchai-muted);
            margin: 0.4rem 0 0 0;
        }

        .feature-card, .step-card, .system-card {
            background: var(--matchai-card);
            border: 1px solid var(--matchai-border);
            border-radius: 20px;
            padding: 1.2rem;
            box-shadow: 0 8px 22px rgba(15, 23, 42, 0.05);
            height: 100%;
        }

        .feature-card h3, .step-card h3, .system-card h3 {
            margin-top: 0;
        }

        .feature-icon {
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }

        .status-chip {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            border-radius: 999px;
            padding: 0.38rem 0.68rem;
            font-size: 0.82rem;
            font-weight: 700;
        }

        .chip-high {
            background: #dcfce7;
            color: #166534;
        }

        .chip-medium {
            background: #fef3c7;
            color: #92400e;
        }

        .chip-low {
            background: #dbeafe;
            color: #1e40af;
        }

        div[data-testid="stMetric"] {
            background: linear-gradient(180deg, #ffffff 0%, #f8fbff 100%);
            border: 1px solid var(--matchai-border);
            border-radius: 18px;
            padding: 1rem 1.05rem;
            box-shadow: 0 8px 20px rgba(15, 23, 42, 0.055);
        }

        div[data-testid="stMetric"] label {
            color: var(--matchai-muted) !important;
            font-weight: 700;
        }

        div[data-testid="stMetric"] [data-testid="stMetricValue"] {
            color: var(--matchai-text);
            font-weight: 800;
        }

        div[data-testid="stForm"], div[data-testid="stExpander"] {
            background: rgba(255, 255, 255, 0.92);
            border: 1px solid var(--matchai-border);
            border-radius: 20px;
            box-shadow: 0 10px 26px rgba(15, 23, 42, 0.055);
        }

        div[data-testid="stForm"] {
            padding: 1.25rem;
        }

        .stButton > button {
            border-radius: 14px;
            font-weight: 800;
            border: 0;
            box-shadow: 0 8px 18px rgba(37, 99, 235, 0.18);
        }

        .stButton > button[kind="primary"], .stButton > button[data-testid="baseButton-primary"] {
            background: linear-gradient(135deg, var(--matchai-primary), var(--matchai-accent));
            color: white;
        }



        [data-testid="stSidebar"],
        [data-testid="collapsedControl"] {
            display: none !important;
        }

        .command-shell {
            max-width: 1180px;
            margin: 0 auto;
        }

        .command-hero {
            background:
                radial-gradient(circle at 90% 15%, rgba(34, 211, 238, 0.30), transparent 28%),
                radial-gradient(circle at 15% 100%, rgba(99, 102, 241, 0.34), transparent 36%),
                linear-gradient(135deg, #07111f 0%, #142b63 52%, #0f6c8d 100%);
            border: 1px solid rgba(255,255,255,0.12);
            border-radius: 30px;
            padding: 3rem 3rem 2.6rem 3rem;
            box-shadow: 0 28px 70px rgba(15, 23, 42, 0.24);
            margin-bottom: 1.4rem;
            overflow: hidden;
            position: relative;
        }

        .command-hero h1 {
            color: white;
            font-size: clamp(2.5rem, 5vw, 4.5rem);
            line-height: 0.98;
            margin: 0 0 1rem 0;
            max-width: 820px;
        }

        .command-hero p {
            color: #dbeafe;
            font-size: 1.08rem;
            max-width: 720px;
            margin: 0;
        }

        .hero-kicker {
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            padding: 0.42rem 0.72rem;
            border-radius: 999px;
            background: rgba(255,255,255,0.12);
            border: 1px solid rgba(255,255,255,0.16);
            color: #cffafe;
            font-size: 0.78rem;
            font-weight: 800;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin-bottom: 1rem;
        }

        .icon-lost { background: linear-gradient(135deg, #ffe4e6, #fecdd3); }
        .icon-found { background: linear-gradient(135deg, #dcfce7, #bbf7d0); }
        .icon-match { background: linear-gradient(135deg, #fef3c7, #fde68a); }
        .icon-report { background: linear-gradient(135deg, #dbeafe, #bfdbfe); }
        .icon-history { background: linear-gradient(135deg, #ede9fe, #ddd6fe); }
        .icon-analytics { background: linear-gradient(135deg, #cffafe, #a5f3fc); }

        .dashboard-card-button div[data-testid="stButton"] {
            height: 100%;
        }

        .dashboard-card-button .stButton > button {
            width: 100%;
            min-height: 184px;
            height: 100%;
            padding: 1.25rem 1.35rem;
            border-radius: 22px;
            border: 1px solid rgba(203, 213, 225, 0.95);
            background: rgba(255,255,255,0.97) !important;
            color: #0f172a !important;
            text-align: left !important;
            justify-content: flex-start !important;
            align-items: flex-start !important;
            white-space: pre-wrap !important;
            box-shadow: 0 12px 28px rgba(15,23,42,0.07);
            transition: transform 0.2s ease, box-shadow 0.2s ease,
                        border-color 0.2s ease;
            line-height: 1.48;
        }

        .dashboard-card-button .stButton > button:hover {
            transform: translateY(-4px);
            box-shadow: 0 20px 38px rgba(15,23,42,0.13);
            border-color: #60a5fa;
        }

        .dashboard-card-button.primary-card .stButton > button {
            background:
                linear-gradient(145deg, rgba(255,255,255,0.99),
                rgba(239,246,255,0.99)) !important;
        }

        .dashboard-card-button .stButton > button p {
            width: 100%;
            text-align: left !important;
            margin: 0;
        }

        .dashboard-card-button .stButton > button strong {
            display: block;
            font-size: 1.08rem;
            margin: 0.65rem 0 0.4rem 0;
            color: #1e293b;
        }

        .section-label {
            margin: 1.5rem 0 0.8rem 0;
            font-size: 0.78rem;
            font-weight: 800;
            letter-spacing: 0.10em;
            text-transform: uppercase;
            color: #2563eb;
        }

        .topbar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0.4rem 0 1rem 0;
        }

        .topbar-brand {
            font-size: 1.1rem;
            font-weight: 900;
            color: #0f172a;
        }

        .live-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            background: #dcfce7;
            color: #166534;
            border-radius: 999px;
            padding: 0.35rem 0.65rem;
            font-size: 0.78rem;
            font-weight: 800;
        }

        .live-dot {
            width: 8px;
            height: 8px;
            border-radius: 999px;
            background: #22c55e;
            box-shadow: 0 0 0 4px rgba(34,197,94,0.14);
        }


        .workflow-strip {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 12px;
            margin-top: 0.25rem;
        }

        .workflow-step {
            position: relative;
            background: rgba(255,255,255,0.88);
            border: 1px solid #dbe4f0;
            border-radius: 18px;
            padding: 1rem;
            box-shadow: 0 8px 18px rgba(15,23,42,0.05);
        }

        .workflow-step:not(:last-child)::after {
            content: "→";
            position: absolute;
            right: -13px;
            top: 50%;
            transform: translateY(-50%);
            color: #2563eb;
            font-weight: 900;
            z-index: 2;
        }

        .workflow-number {
            font-size: 0.72rem;
            font-weight: 900;
            color: #2563eb;
            letter-spacing: 0.08em;
        }

        .workflow-title {
            font-size: 1rem;
            font-weight: 800;
            color: #0f172a;
            margin-top: 0.3rem;
        }

        .workflow-copy {
            color: #64748b;
            font-size: 0.84rem;
            margin-top: 0.18rem;
        }


        .brand-mark {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 30px;
            height: 30px;
            border-radius: 10px;
            margin-right: 8px;
            color: #ffffff;
            background: linear-gradient(135deg, #2563eb, #06b6d4);
            font-size: 0.88rem;
            font-weight: 900;
            box-shadow: 0 8px 18px rgba(37,99,235,0.25);
        }

        .action-symbol {
            width: 46px;
            height: 46px;
            border-radius: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 0.85rem;
            font-size: 0.78rem;
            font-weight: 900;
            letter-spacing: 0.04em;
            box-shadow: 0 8px 18px rgba(15,23,42,0.10);
        }

        .smart-report-shell {
            background: rgba(255,255,255,0.92);
            border: 1px solid #dbe4f0;
            border-radius: 24px;
            padding: 1.35rem;
            box-shadow: 0 12px 30px rgba(15,23,42,0.07);
            margin-bottom: 1rem;
        }

        .smart-report-title {
            font-size: 0.78rem;
            font-weight: 900;
            color: #2563eb;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin-bottom: 0.4rem;
        }

        .smart-report-copy {
            color: #64748b;
            margin-bottom: 0;
        }

        .ai-result-card {
            background: linear-gradient(135deg, rgba(239,246,255,0.96), rgba(236,254,255,0.96));
            border: 1px solid #bfdbfe;
            border-radius: 20px;
            padding: 1rem 1.1rem;
            margin: 0.8rem 0 1rem 0;
        }

        .ai-result-label {
            color: #1d4ed8;
            font-size: 0.75rem;
            font-weight: 900;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }


        .report-hero {
            border-radius: 26px;
            padding: 2.2rem 2.3rem;
            margin: 1.1rem 0 1.25rem 0;
            border: 1px solid #dbe4f0;
            box-shadow: 0 14px 34px rgba(15,23,42,0.08);
            background: #ffffff;
        }

        .report-hero-lost {
            background:
                radial-gradient(circle at 90% 10%, rgba(251,113,133,0.18), transparent 32%),
                linear-gradient(145deg, #ffffff, #fff7f8);
            border-left: 6px solid #f43f5e;
        }

        .report-hero-found {
            background:
                radial-gradient(circle at 90% 10%, rgba(52,211,153,0.18), transparent 32%),
                linear-gradient(145deg, #ffffff, #f4fff9);
            border-left: 6px solid #10b981;
        }

        .report-eyebrow {
            font-size: 0.75rem;
            font-weight: 900;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            margin-bottom: 0.55rem;
        }

        .report-eyebrow-lost {
            color: #e11d48;
        }

        .report-eyebrow-found {
            color: #059669;
        }

        .report-hero h1 {
            margin: 0;
            color: #1e293b;
            font-size: 2.2rem;
        }

        .report-hero p {
            margin: 0.55rem 0 0 0;
            color: #64748b;
            max-width: 820px;
            line-height: 1.65;
        }

        .report-step {
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            margin-top: 1rem;
            padding: 0.42rem 0.72rem;
            border-radius: 999px;
            background: #eff6ff;
            color: #1d4ed8;
            font-size: 0.78rem;
            font-weight: 800;
        }

        .section-panel {
            background: rgba(255,255,255,0.94);
            border: 1px solid #dbe4f0;
            border-radius: 22px;
            padding: 1.2rem 1.25rem;
            box-shadow: 0 10px 26px rgba(15,23,42,0.055);
            margin-bottom: 1rem;
        }

        .section-panel-title {
            color: #1e293b;
            font-size: 1.05rem;
            font-weight: 850;
            margin-bottom: 0.2rem;
        }

        .section-panel-copy {
            color: #64748b;
            font-size: 0.88rem;
            margin-bottom: 0;
        }

        .lost-guidance {
            background: #fff1f2;
            border: 1px solid #fecdd3;
            color: #9f1239;
        }

        .found-guidance {
            background: #ecfdf5;
            border: 1px solid #a7f3d0;
            color: #065f46;
        }

        .guidance-box {
            border-radius: 16px;
            padding: 0.85rem 1rem;
            margin: 0.65rem 0 1rem 0;
            font-size: 0.88rem;
            line-height: 1.55;
        }

        .top-back-button div[data-testid="stButton"] > button {
            min-height: 50px !important;
            height: 50px !important;
            border-radius: 13px !important;
            background: linear-gradient(135deg, #2563eb, #06b6d4) !important;
            color: #ffffff !important;
            border: 0 !important;
            box-shadow: 0 10px 22px rgba(37,99,235,0.24) !important;
            text-align: center !important;
            justify-content: center !important;
            align-items: center !important;
            padding: 0.7rem 1.1rem !important;
        }

        .top-back-button div[data-testid="stButton"] > button p {
            color: #ffffff !important;
            text-align: center !important;
            font-weight: 850 !important;
        }

        .save-report-button div[data-testid="stButton"] > button {
            min-height: 48px !important;
            border-radius: 14px !important;
            color: #ffffff !important;
            font-weight: 850 !important;
        }


        html, body, [class*="css"] {
            font-size: 17px;
        }

        .block-container {
            max-width: 1220px;
            padding-left: 2rem;
            padding-right: 2rem;
        }

        h1 {
            font-size: 2.45rem !important;
            line-height: 1.1 !important;
        }

        h2 {
            font-size: 1.9rem !important;
        }

        h3 {
            font-size: 1.4rem !important;
        }

        p,
        label,
        .stMarkdown,
        .stText,
        .stCaption {
            font-size: 1rem !important;
            line-height: 1.6 !important;
        }

        div[data-testid="stTextInput"] input,
        div[data-testid="stTextArea"] textarea,
        div[data-testid="stSelectbox"] div,
        div[data-testid="stDateInput"] input,
        div[data-testid="stFileUploader"] {
            font-size: 1rem !important;
        }

        div[data-testid="stButton"] > button {
            font-size: 1rem !important;
            font-weight: 800 !important;
        }

        .topbar-brand {
            font-size: 1.15rem !important;
        }

        .live-badge {
            font-size: 0.9rem !important;
        }

        .report-eyebrow {
            font-size: 0.85rem !important;
        }

        .report-hero h1 {
            font-size: 2.55rem !important;
        }

        .report-hero p {
            font-size: 1.08rem !important;
        }

        .report-step {
            font-size: 0.88rem !important;
        }

        .section-panel-title {
            font-size: 1.2rem !important;
        }

        .section-panel-copy {
            font-size: 0.98rem !important;
        }

        .guidance-box {
            font-size: 0.98rem !important;
        }


        /* Stable three-column topbar alignment. */
        .topbar-left,
        .topbar-center {
            min-height: 52px;
            display: flex;
            align-items: center;
        }

        .topbar-left {
            justify-content: flex-start;
        }

        .topbar-center {
            justify-content: center;
        }

        .topbar-brand-text {
            color: #0f172a;
            font-size: 1.15rem;
            font-weight: 850;
            margin-left: 0.55rem;
        }

        .topbar-right-spacer {
            min-height: 52px;
        }

        /* Target the actual Streamlit back-button widget by its key class. */
        [class*="st-key-back_"] div[data-testid="stButton"] > button {
            min-height: 50px !important;
            height: 50px !important;
            border-radius: 14px !important;
            background: linear-gradient(135deg, #2563eb, #06b6d4) !important;
            color: #ffffff !important;
            border: 0 !important;
            box-shadow: 0 10px 22px rgba(37,99,235,0.24) !important;
            text-align: center !important;
            justify-content: center !important;
            align-items: center !important;
            padding: 0.7rem 1rem !important;
        }

        [class*="st-key-back_"] div[data-testid="stButton"] > button p {
            color: #ffffff !important;
            text-align: center !important;
            font-weight: 850 !important;
            margin: 0 !important;
        }


        /* =========================================================
           FINAL DASHBOARD CARD OVERRIDES
           Keeps the original WHITE card design from the screenshot.
           Applies only to the six dashboard action cards.
           ========================================================= */

        [class*="st-key-open_lost"] button,
        [class*="st-key-open_found"] button,
        [class*="st-key-open_matching"] button,
        [class*="st-key-open_reports"] button,
        [class*="st-key-open_history"] button,
        [class*="st-key-open_analytics"] button {
            width: 100% !important;
            min-height: 210px !important;
            height: auto !important;

            padding: 1.35rem 1.4rem !important;
            border-radius: 24px !important;
            border: 1px solid #d7e0ec !important;

            background: #ffffff !important;
            color: #1e293b !important;

            text-align: left !important;
            justify-content: flex-start !important;
            align-items: flex-start !important;

            white-space: normal !important;
            overflow: hidden !important;

            box-shadow:
                0 14px 30px rgba(15, 23, 42, 0.08) !important;

            transition:
                transform 0.2s ease,
                box-shadow 0.2s ease,
                border-color 0.2s ease !important;
        }

        /* Blue top border for core actions. */
        [class*="st-key-open_lost"] button,
        [class*="st-key-open_found"] button,
        [class*="st-key-open_matching"] button {
            border-top: 4px solid #2563eb !important;
        }

        /* Teal top border for management actions. */
        [class*="st-key-open_reports"] button,
        [class*="st-key-open_history"] button,
        [class*="st-key-open_analytics"] button {
            border-top: 4px solid #14b8a6 !important;
        }

        [class*="st-key-open_lost"] button:hover,
        [class*="st-key-open_found"] button:hover,
        [class*="st-key-open_matching"] button:hover,
        [class*="st-key-open_reports"] button:hover,
        [class*="st-key-open_history"] button:hover,
        [class*="st-key-open_analytics"] button:hover {
            transform: translateY(-4px) !important;
            border-color: #60a5fa !important;

            box-shadow:
                0 22px 42px rgba(15, 23, 42, 0.14) !important;
        }

        /* Keep all text inside the card. */
        [class*="st-key-open_lost"] button p,
        [class*="st-key-open_found"] button p,
        [class*="st-key-open_matching"] button p,
        [class*="st-key-open_reports"] button p,
        [class*="st-key-open_history"] button p,
        [class*="st-key-open_analytics"] button p {
            width: 100% !important;
            max-width: 100% !important;

            margin: 0 !important;

            color: #64748b !important;
            text-align: left !important;

            font-size: 0.98rem !important;
            line-height: 1.5 !important;

            white-space: normal !important;
            overflow-wrap: anywhere !important;
            word-break: normal !important;
        }

        /* Card title. */
        [class*="st-key-open_lost"] button strong,
        [class*="st-key-open_found"] button strong,
        [class*="st-key-open_matching"] button strong,
        [class*="st-key-open_reports"] button strong,
        [class*="st-key-open_history"] button strong,
        [class*="st-key-open_analytics"] button strong {
            display: block !important;

            margin:
                0.7rem
                0
                0.45rem
                0 !important;

            color: #1e293b !important;

            font-size: 1.15rem !important;
            line-height: 1.3 !important;
            font-weight: 850 !important;

            white-space: normal !important;
            overflow-wrap: anywhere !important;
        }

        /* LOST, FOUND, AI, DATA, LOG, ML labels. */
        [class*="st-key-open_lost"] button code,
        [class*="st-key-open_found"] button code,
        [class*="st-key-open_matching"] button code,
        [class*="st-key-open_reports"] button code,
        [class*="st-key-open_history"] button code,
        [class*="st-key-open_analytics"] button code {
            display: inline-block !important;

            padding: 0.36rem 0.62rem !important;
            border-radius: 10px !important;

            background: #e5efff !important;
            color: #1d4ed8 !important;

            font-family: inherit !important;
            font-size: 0.73rem !important;
            font-weight: 900 !important;
            letter-spacing: 0.08em !important;
        }

        @media (max-width: 900px) {
            [class*="st-key-open_lost"] button,
            [class*="st-key-open_found"] button,
            [class*="st-key-open_matching"] button,
            [class*="st-key-open_reports"] button,
            [class*="st-key-open_history"] button,
            [class*="st-key-open_analytics"] button {
                min-height: 190px !important;
                height: auto !important;
            }
        }


        @media (max-width: 700px) {
            .command-hero { padding: 2rem 1.4rem; }
            .command-hero h1 { font-size: 2.6rem; }
            .block-container {
                padding-top: 4rem;
                padding-left: 1rem;
                padding-right: 1rem;
            }
            .workflow-strip { grid-template-columns: 1fr; }
            .workflow-step:not(:last-child)::after { display: none; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
