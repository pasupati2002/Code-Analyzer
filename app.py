import streamlit as st
from src.analyzer import analyze_code

st.set_page_config(page_title="Code Analyzer", page_icon="🔍")
st.title("🔍 Code Analyzer")

language = st.selectbox("Language", ["Python", "JavaScript", "Java", "C++", "Other"])
uploaded = st.file_uploader("Upload a code file (optional)")
code = st.text_area("Or paste your code here", height=300)

if uploaded:
    code = uploaded.read().decode("utf-8")

if st.button("Analyze"):
    if not code.strip():
        st.warning("Please provide some code first.")
    else:
        with st.spinner("Analyzing..."):
            try:
                st.markdown(analyze_code(code, language))
            except Exception as e:
                st.error(f"Something went wrong: {e}")