import streamlit as st
import requests

url = "http://13.63.94.119:8000/enhance"


def enhance_text(original_text):
    res = requests.get(url=url, params={"original_text": original_text})
    return res.json()

st.markdown("""
    <style>
        .block-container {
            padding-top: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="Meaning-Preserving-AI-Notes-Enhancer", layout="wide")
st.markdown(
    "<h1 style='text-align: center;'>Meaning Preserving AI-Notes Enhancer</h1>",
    unsafe_allow_html=True,
)

st.markdown(
    "<h3 style='text-align: center;'>Created by - Team FixIt</h3></br>",
    unsafe_allow_html=True,
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Mono:wght@300;400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Mono', monospace;
        background-color: #0e0e0e;
        color: #e8e0d0;
    }

    .stApp {
        background: #0e0e0e;
    }

    h1 {
        font-family: 'DM Serif Display', serif;
        font-style: italic;
        font-size: 2.8rem !important;
        color: #f5c842 !important;
        letter-spacing: -1px;
        text-align: center;
        margin-bottom: 0.2rem !important;
    }

    .subtitle {
        text-align: center;
        color: #666;
        font-size: 0.78rem;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        margin-bottom: 2.5rem;
    }

    .col-label {
        font-size: 0.68rem;
        letter-spacing: 0.22em;
        text-transform: uppercase;
        color: #555;
        margin-bottom: 6px;
    }

    textarea {
        background-color: #1a1a1a !important;
        color: #e8e0d0 !important;
        border: 1px solid #2e2e2e !important;
        border-radius: 4px !important;
        font-family: 'DM Mono', monospace !important;
        font-size: 0.9rem !important;
        resize: none !important;
        caret-color: #f5c842 !important;
    }

    textarea:focus {
        border-color: #f5c842 !important;
        box-shadow: 0 0 0 1px #f5c84233 !important;
    }

    .output-box {
        background: #1a1a1a;
        border: 1px solid #2e2e2e;
        border-radius: 4px;
        padding: 14px 16px;
        height: 280px;
        overflow: auto;
        font-family: 'DM Mono', monospace;
        font-size: 0.9rem;
        color: #e8e0d0;
        line-height: 1.7;
        white-space: pre-wrap;
        word-break: break-word;
    }

    .output-box.empty {
        color: #3a3a3a;
        font-style: italic;
    }

    .stButton > button {
        width: 100%;
        background: #f5c842 !important;
        color: #0e0e0e !important;
        font-family: 'DM Mono', monospace !important;
        font-size: 0.82rem !important;
        font-weight: 500 !important;
        letter-spacing: 0.18em !important;
        text-transform: uppercase !important;
        border: none !important;
        border-radius: 4px !important;
        padding: 0.65rem 1.2rem !important;
        cursor: pointer !important;
        transition: background 0.15s ease, transform 0.1s ease !important;
    }

    .stButton > button:hover {
        background: #ffd966 !important;
        transform: translateY(-1px) !important;
    }

    .stButton > button:active {
        transform: translateY(0px) !important;
    }

    .divider {
        width: 1px;
        background: #2e2e2e;
        height: 100%;
    }

    .stSpinner > div {
        border-top-color: #f5c842 !important;
    }

    #MainMenu, footer, header { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)


left_col, mid_col, right_col = st.columns([5, 1.4, 5])

with left_col:
    st.markdown('<p class="col-label">Input</p>', unsafe_allow_html=True)
    user_input = st.text_area(
        label="",
        placeholder="Paste or type your text here…",
        height=280,
        key="input_text",
        label_visibility="collapsed",
    )

with mid_col:
    st.markdown("<div style='height:148px'></div>", unsafe_allow_html=True)
    enhance_clicked = st.button("✦ Enhance")

response = None
with right_col:
    st.markdown('<p class="col-label">Output</p>', unsafe_allow_html=True)

    output_placeholder = st.empty()
    if enhance_clicked and len(user_input.strip()) != 0:
        with st.spinner("Enhancing…"):
            try:
                res = enhance_text(user_input)
            except Exception as E:
                res = {"enhanced_text": "Unable to enhance"}
                print(E)
        orignal_words = user_input.split()
        enhanced_words = res["enhanced_text"].split()
        res_str = [
            (
                f'<span style="color: #87CEEB;">{i}</span>'
                if i not in orignal_words
                else f'<span style="color: orange;">{i}</span>'
            )
            for i in enhanced_words
        ]
        res_str = " ".join(res_str)
        output_placeholder.markdown(
            f'<div class="output-box">{res_str}</div>',
            unsafe_allow_html=True,
        )
if enhance_clicked and len(user_input.strip()) != 0:
    try:
        st.markdown(
            '<h3 style="text-align:center; letter-spacing:0.2em; text-transform:uppercase;">Semantic similarity score </h3>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<p style="text-align:center; font-size:3rem; font-family:serif; font-style:italic; color:#f5c842; margin:0;">{res["similarity_score"]*100:.2f}%</p>',
            unsafe_allow_html=True,
        )
    except Exception as E:
        print(E)
