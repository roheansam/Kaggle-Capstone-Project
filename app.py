import streamlit as st
from agent import generate_project_blueprint
from datetime import datetime
import base64
from pathlib import Path
from PIL import Image


# -----------------------------
# Logo Setup
# -----------------------------
LOGO_PATH = Path("assets/brain.png")
FONT_PATH = Path("assets/fonts/GoogleSansFlex.ttf")


if LOGO_PATH.exists() and LOGO_PATH.stat().st_size > 0:
    page_icon = Image.open(LOGO_PATH)
else:
    page_icon = "🤖"


st.set_page_config(
    page_title="ProjectPilot AI",
    page_icon=page_icon,
    layout="wide",
    initial_sidebar_state="expanded"
)


# -----------------------------
# Load Local Google Sans Flex Font
# -----------------------------
def load_local_font(font_path: Path):
    if not font_path.exists():
        return

    if font_path.stat().st_size < 1000:
        return

    encoded_font = base64.b64encode(font_path.read_bytes()).decode()

    st.markdown(
        f"""
        <style>
        @font-face {{
            font-family: 'Google Sans Flex';
            src: url(data:font/ttf;base64,{encoded_font}) format('truetype');
            font-weight: 100 1000;
            font-style: normal;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


def get_logo_html():
    if LOGO_PATH.exists() and LOGO_PATH.stat().st_size > 0:
        image_data = base64.b64encode(LOGO_PATH.read_bytes()).decode()
        return f'<img src="data:image/png;base64,{image_data}" class="brand-logo" alt="ProjectPilot AI Logo">'
    return '<span class="brand-fallback">AI</span>'


load_local_font(FONT_PATH)


# -----------------------------
# CSS Styling
# -----------------------------
st.markdown(
    """
<style>
/* Google Sans Flex without breaking Streamlit icons */
html,
body,
.stApp,
.block-container,
div[data-testid="stMarkdownContainer"],
div[data-testid="stMarkdownContainer"] p,
div[data-testid="stMarkdownContainer"] li,
div[data-testid="stMarkdownContainer"] h1,
div[data-testid="stMarkdownContainer"] h2,
div[data-testid="stMarkdownContainer"] h3,
div[data-testid="stMarkdownContainer"] h4,
div[data-testid="stMarkdownContainer"] h5,
div[data-testid="stMarkdownContainer"] h6,
div[data-testid="stMarkdownContainer"] strong,
.stTextArea textarea,
.stButton button,
.stDownloadButton button {
    font-family: "Google Sans Flex", "Google Sans", "Product Sans", "Roboto", Arial, sans-serif !important;
}

/* Keep Streamlit internal icons working */
span[class*="material-symbols"],
span[class*="material-icons"],
i[class*="material-icons"],
[class*="material-symbols"],
[class*="material-icons"],
[data-testid="stIconMaterial"],
[data-testid="stIconMaterialOutlined"],
[data-testid="stIconMaterialRounded"] {
    font-family: "Material Symbols Rounded", "Material Symbols Outlined", "Material Icons" !important;
    font-weight: normal !important;
    font-style: normal !important;
    letter-spacing: normal !important;
    text-transform: none !important;
    white-space: nowrap !important;
    word-wrap: normal !important;
    direction: ltr !important;
    -webkit-font-feature-settings: "liga" !important;
    -webkit-font-smoothing: antialiased !important;
    font-feature-settings: "liga" !important;
}

/* App Background */
.stApp {
    background: #f8fafd;
}

/* Main text visibility fix */
div[data-testid="stMarkdownContainer"],
div[data-testid="stMarkdownContainer"] p,
div[data-testid="stMarkdownContainer"] li,
div[data-testid="stMarkdownContainer"] span,
div[data-testid="stMarkdownContainer"] h1,
div[data-testid="stMarkdownContainer"] h2,
div[data-testid="stMarkdownContainer"] h3,
div[data-testid="stMarkdownContainer"] h4,
div[data-testid="stMarkdownContainer"] h5,
div[data-testid="stMarkdownContainer"] h6,
div[data-testid="stMarkdownContainer"] strong {
    color: #202124 !important;
}

/* Inline code words inside generated output */
div[data-testid="stMarkdownContainer"] code {
    font-family: "SF Mono", "Menlo", "Monaco", "Consolas", monospace !important;
    color: #137333 !important;
    background-color: #e6f4ea !important;
    padding: 3px 7px;
    border-radius: 7px;
    font-size: 0.92em;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #ffffff;
    border-right: 1px solid #e8eaed;
}

/* Main content width */
.block-container {
    padding-top: 3rem;
    padding-bottom: 3rem;
    max-width: 1200px;
}

/* Header Card */
.google-header {
    background: #ffffff;
    border: 1px solid #e8eaed;
    border-radius: 28px;
    padding: 38px 44px;
    margin-bottom: 26px;
    box-shadow: 0 1px 3px rgba(60, 64, 67, 0.12);
}

.brand-row {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 24px;
}

.brand-icon {
    width: 58px;
    height: 58px;
    border-radius: 18px;
    background: linear-gradient(135deg, #4285F4, #34A853);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white !important;
    font-size: 24px;
    font-weight: 700;
    box-shadow: 0 6px 18px rgba(66, 133, 244, 0.25);
    overflow: hidden;
}

.brand-logo {
    width: 38px;
    height: 38px;
    object-fit: contain;
    display: block;
}

.brand-fallback {
    color: white !important;
    font-size: 22px;
    font-weight: 800;
}

.brand-name {
    font-size: 22px;
    color: #5f6368 !important;
    font-weight: 600;
}

.hero-title {
    font-size: 46px;
    line-height: 1.12;
    font-weight: 700;
    color: #202124 !important;
    letter-spacing: -1.4px;
    margin-bottom: 16px;
}

.hero-subtitle {
    font-size: 18px;
    line-height: 1.7;
    color: #5f6368 !important;
    max-width: 900px;
}

.highlight-blue {
    color: #1a73e8 !important;
}

/* Feature Cards */
.feature-card {
    background: #ffffff;
    border: 1px solid #e8eaed;
    border-radius: 24px;
    padding: 24px;
    min-height: 165px;
    box-shadow: 0 1px 3px rgba(60, 64, 67, 0.10);
    transition: all 0.2s ease;
    margin-bottom: 12px;
}

.feature-card:hover {
    box-shadow: 0 8px 22px rgba(60, 64, 67, 0.15);
    transform: translateY(-2px);
}

.feature-icon {
    width: 42px;
    height: 42px;
    border-radius: 14px;
    background: #e8f0fe;
    color: #1a73e8 !important;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    margin-bottom: 14px;
}

.feature-title {
    font-size: 19px;
    font-weight: 600;
    color: #202124 !important;
    margin-bottom: 8px;
}

.feature-text {
    font-size: 15px;
    line-height: 1.6;
    color: #5f6368 !important;
}

/* Input Section */
.input-card {
    background: #ffffff;
    border: 1px solid #e8eaed;
    border-radius: 28px;
    padding: 30px;
    margin-top: 26px;
    margin-bottom: 20px;
    box-shadow: 0 1px 3px rgba(60, 64, 67, 0.10);
}

.section-title {
    font-size: 27px;
    font-weight: 650;
    color: #202124 !important;
    margin-bottom: 8px;
}

.section-subtitle {
    font-size: 15px;
    color: #5f6368 !important;
    margin-bottom: 4px;
}

/* Sidebar custom text */
.sidebar-title {
    font-size: 25px;
    font-weight: 700;
    color: #202124 !important;
    margin-bottom: 8px;
}

.sidebar-subtitle {
    color: #5f6368 !important;
    font-size: 15px;
    line-height: 1.6;
    margin-bottom: 18px;
}

.mini-label {
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    color: #5f6368 !important;
    font-weight: 700;
    margin-top: 18px;
    margin-bottom: 10px;
}

.capability {
    background: #f1f3f4;
    border-radius: 999px;
    padding: 8px 13px;
    color: #3c4043 !important;
    font-size: 14px;
    margin-bottom: 8px;
    display: inline-block;
}

/* Text area */
.stTextArea textarea {
    border-radius: 18px !important;
    border: 1px solid #dadce0 !important;
    padding: 16px !important;
    font-size: 16px !important;
    color: #202124 !important;
    background-color: #ffffff !important;
}

.stTextArea textarea:focus {
    border: 2px solid #1a73e8 !important;
    box-shadow: none !important;
}

/* Buttons */
.stButton > button {
    border-radius: 999px;
    border: none;
    background: #1a73e8;
    color: white !important;
    font-weight: 600;
    min-height: 46px;
    padding: 0 24px;
    box-shadow: 0 1px 2px rgba(60, 64, 67, 0.25);
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background: #185abc;
    color: white !important;
    box-shadow: 0 4px 12px rgba(66, 133, 244, 0.28);
}

.stDownloadButton > button {
    border-radius: 999px;
    border: 1px solid #dadce0;
    background: #ffffff;
    color: #1a73e8 !important;
    font-weight: 600;
    min-height: 44px;
}

.stDownloadButton > button:hover {
    background: #f8fafd;
    border: 1px solid #1a73e8;
    color: #1a73e8 !important;
}

/* Output container */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #ffffff !important;
    border-radius: 24px !important;
    border: 1px solid #e8eaed !important;
    box-shadow: 0 1px 3px rgba(60, 64, 67, 0.10) !important;
}

/* Alert boxes */
div[data-testid="stAlert"] {
    border-radius: 18px !important;
}

/* Expander */
div[data-testid="stExpander"] {
    background: #ffffff;
    border: 1px solid #e8eaed;
    border-radius: 18px;
    box-shadow: 0 1px 2px rgba(60, 64, 67, 0.08);
}

/* Footer */
.footer-note {
    color: #5f6368 !important;
    font-size: 14px;
    text-align: center;
    padding: 22px 0;
}

hr {
    border-color: #e8eaed;
}
</style>
""",
    unsafe_allow_html=True
)


# -----------------------------
# Session State
# -----------------------------
if "history" not in st.session_state:
    st.session_state.history = []

if "idea_text" not in st.session_state:
    st.session_state.idea_text = ""


def set_example(text):
    st.session_state.idea_text = text


# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.markdown(
        '<div class="sidebar-title">ProjectPilot AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-subtitle">A Google-style AI agent that converts raw project ideas into complete project blueprints.</div>',
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown(
        '<div class="mini-label">Example Ideas</div>',
        unsafe_allow_html=True
    )

    st.button(
        "Customer Churn Prediction",
        use_container_width=True,
        on_click=set_example,
        args=("I want to make a project on customer churn prediction.",)
    )

    st.button(
        "Axion Fitness Analytics",
        use_container_width=True,
        on_click=set_example,
        args=(
            "I want to build Axion, an AI-based human movement and fitness analytics system "
            "that uses computer vision and pose detection to analyze exercise posture, calculate joint angles, "
            "detect incorrect form, and give feedback to improve fitness performance and reduce injury risk.",
        )
    )

    st.button(
        "SpendX Expense Tracker",
        use_container_width=True,
        on_click=set_example,
        args=(
            "I want to build SpendX, an AI-powered expense tracking system that helps users record expenses, "
            "categorize spending, analyze financial habits, detect overspending, and generate smart budget suggestions.",
        )
    )

    st.divider()

    st.markdown(
        '<div class="mini-label">Agent Capabilities</div>',
        unsafe_allow_html=True
    )

    st.markdown('<span class="capability">Planning</span>', unsafe_allow_html=True)
    st.markdown('<span class="capability">Dataset Guidance</span>', unsafe_allow_html=True)
    st.markdown('<span class="capability">Model Suggestions</span>', unsafe_allow_html=True)
    st.markdown('<span class="capability">Workflow Design</span>', unsafe_allow_html=True)
    st.markdown('<span class="capability">Evaluation Metrics</span>', unsafe_allow_html=True)
    st.markdown('<span class="capability">Safety Checks</span>', unsafe_allow_html=True)


# -----------------------------
# Header
# -----------------------------
logo_html = get_logo_html()

header_html = (
    '<div class="google-header">'
    '<div class="brand-row">'
    '<div class="brand-icon">' + logo_html + '</div>'
    '<div class="brand-name">ProjectPilot AI</div>'
    '</div>'
    '<div class="hero-title">'
    'Build better project plans with <span class="highlight-blue">AI guidance</span>'
    '</div>'
    '<div class="hero-subtitle">'
    'Turn a rough idea into a complete AI/ML project blueprint with problem statement, '
    'dataset requirements, model recommendations, workflow planning, evaluation metrics, '
    'limitations, and final summary.'
    '</div>'
    '</div>'
)

st.markdown(header_html, unsafe_allow_html=True)


# -----------------------------
# Feature Cards
# -----------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        '<div class="feature-card">'
        '<div class="feature-icon">🧠</div>'
        '<div class="feature-title">Smart Planning</div>'
        '<div class="feature-text">Converts simple ideas into structured project plans for students and beginners.</div>'
        '</div>',
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        '<div class="feature-card">'
        '<div class="feature-icon">📊</div>'
        '<div class="feature-title">Dataset Guidance</div>'
        '<div class="feature-text">Suggests data requirements, possible sources, and important dataset columns.</div>'
        '</div>',
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        '<div class="feature-card">'
        '<div class="feature-icon">✅</div>'
        '<div class="feature-title">Evaluation Ready</div>'
        '<div class="feature-text">Recommends evaluation metrics, risks, limitations, and improvement areas.</div>'
        '</div>',
        unsafe_allow_html=True
    )


# -----------------------------
# Input Area
# -----------------------------
st.markdown(
    '<div class="input-card">'
    '<div class="section-title">Create your project blueprint</div>'
    '<div class="section-subtitle">Enter a project idea below. The agent will analyze it and generate a complete blueprint.</div>'
    '</div>',
    unsafe_allow_html=True
)

user_idea = st.text_area(
    "Project idea",
    key="idea_text",
    placeholder="Example: I want to make a project on customer churn prediction.",
    height=150,
    label_visibility="collapsed"
)

generate_btn = st.button(
    "Generate Project Blueprint",
    use_container_width=True
)


# -----------------------------
# Generate Output
# -----------------------------
if generate_btn:
    if user_idea.strip():
        with st.spinner("ProjectPilot AI is creating your blueprint..."):
            result = generate_project_blueprint(user_idea)
            timestamp = datetime.now().strftime("%d %b %Y, %I:%M %p")

            st.session_state.history.append(
                {
                    "idea": user_idea,
                    "blueprint": result,
                    "time": timestamp
                }
            )

        st.success("Blueprint generated successfully!")

        with st.container(border=True):
            st.markdown("## Generated Project Blueprint")
            st.markdown(result)

        st.download_button(
            label="Download Blueprint",
            data=result,
            file_name="project_blueprint.txt",
            mime="text/plain"
        )

    else:
        st.warning("Please enter a project idea first.")


# -----------------------------
# History
# -----------------------------
if st.session_state.history:
    st.divider()

    st.markdown(
        '<div class="section-title">Generated Blueprint History</div>',
        unsafe_allow_html=True
    )

    for index, item in enumerate(reversed(st.session_state.history), start=1):
        short_idea = item["idea"][:80]

        with st.expander(f"Blueprint {index}: {short_idea}..."):
            st.caption(f"Generated on: {item['time']}")
            st.markdown(item["blueprint"])

            st.download_button(
                label=f"Download Blueprint {index}",
                data=item["blueprint"],
                file_name=f"project_blueprint_{index}.txt",
                mime="text/plain",
                key=f"download_{index}"
            )


# -----------------------------
# Footer
# -----------------------------
st.markdown(
    '<div class="footer-note">ProjectPilot AI · Built for the Kaggle AI Agents Capstone Project</div>',
    unsafe_allow_html=True
)