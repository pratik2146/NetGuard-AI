import streamlit as st

def inject_custom_css() -> None:
    """
    Inject clean, modern, simplified CSS into Streamlit application.
    """
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        .block-container {
            max-width: 1400px;
            padding-top: 1.5rem;
            padding-bottom: 2.5rem;
        }

        /* Clean Header */
        .main-header {
            padding: 20px 24px;
            border-radius: 14px;
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            color: #ffffff;
            margin-bottom: 24px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }

        .main-header h1 {
            margin: 0;
            font-size: 28px;
            font-weight: 700;
            color: #ffffff;
        }

        .main-header p {
            margin-top: 6px;
            margin-bottom: 0;
            color: #94a3b8;
            font-size: 14px;
        }

        /* Clean Metric Card */
        .simple-card {
            padding: 16px 20px;
            border-radius: 12px;
            background: rgba(30, 41, 59, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.08);
            margin-bottom: 14px;
        }

        .card-label {
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 0.5px;
            color: #94a3b8;
            text-transform: uppercase;
        }

        .card-value {
            font-size: 26px;
            font-weight: 800;
            color: #f8fafc;
            margin-top: 4px;
        }

        .card-sub {
            font-size: 12px;
            color: #64748b;
            margin-top: 2px;
        }

        /* Section Titles */
        .section-header {
            font-size: 18px;
            font-weight: 700;
            color: #f8fafc;
            margin-top: 22px;
            margin-bottom: 12px;
        }

        /* Simple Footer */
        .simple-footer {
            text-align: center;
            color: #64748b;
            font-size: 12px;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid rgba(255, 255, 255, 0.08);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def render_header(title: str, subtitle: str, tag: str = "") -> None:
    st.markdown(
        f"""
        <div class="main-header">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_simple_card(label: str, value: str, subtitle: str = "") -> None:
    st.markdown(
        f"""
        <div class="simple-card">
            <div class="card-label">{label}</div>
            <div class="card-value">{value}</div>
            <div class="card-sub">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Backward Compatibility Aliases
render_hero = render_header
render_metric_card = render_simple_card
