import streamlit as st
import pandas as pd
import os
import re
import base64
import streamlit.components.v1 as components
from streamlit_pdf import pdf_viewer
from deep_translator import GoogleTranslator
from pathlib import Path

# ==== CONFIG ====
CSV_PATH = "/Users/froquser/Desktop/txt_extract/data.csv"  # your CSV file path
PDF_DIR = "/Users/froquser/Desktop/txt_extract/test2"       # folder containing artwork PDFs

st.set_page_config(page_title="🎨 Artwork Search Engine", layout="wide")

st.title("🎨 Artwork Search Engine with PDF Preview")

# ==== LOAD DATA ====
@st.cache_data
def load_data():
    if not os.path.exists(CSV_PATH):
        st.error(f"No CSV found at '{CSV_PATH}'. Please place your file in this folder.")
        st.stop()
    df = pd.read_csv(CSV_PATH)
    df.columns = [c.strip().lower() for c in df.columns]
    return df

df = load_data()

# ==== VALIDATE COLUMNS ====
required_cols = ["file name", "product description"]
for col in required_cols:
    if col not in df.columns:
        st.error(f"❌ Missing required column: '{col}' — found only {df.columns.tolist()}")
        st.stop()

# ==== SEARCH BAR ====
query = st.text_input("🔍 Search artworks", placeholder="Type keyword (e.g., 'chicken' or 'kip')...")

if query:
    query_lower = query.strip().lower()
    safe_query = re.escape(query_lower)

    # ===== EXACT MATCH =====
    exact_pattern = rf"(?<!\w){safe_query}(?!\w)"
    exact_results = df[
        df["file name"].str.lower().str.contains(exact_pattern, regex=True, na=False)
        | df["product description"].str.lower().str.contains(exact_pattern, regex=True, na=False)
    ]

    # ===== PARTIAL MATCH =====
    partial_results = df[
        df["file name"].str.lower().str.contains(safe_query, na=False)
        | df["product description"].str.lower().str.contains(safe_query, na=False)
    ]
    partial_results = partial_results.loc[~partial_results.index.isin(exact_results.index)]

    # ===== TRANSLATED MATCH (BIDIRECTIONAL) =====
    languages = ["en", "nl", "fr", "de", "es", "it"]
    translated_terms = set()

    for lang in languages:
        try:
            translated_fwd = GoogleTranslator(source="auto", target=lang).translate(query_lower)
            translated_terms.add(translated_fwd.lower())
            translated_back = GoogleTranslator(source=lang, target="en").translate(query_lower)
            translated_terms.add(translated_back.lower())
        except Exception:
            continue

    translated_terms.discard(query_lower)
    translated_results = pd.DataFrame()
    for term in translated_terms:
        safe_term = re.escape(term)
        match = df[
            df["file name"].str.lower().str.contains(safe_term, na=False)
            | df["product description"].str.lower().str.contains(safe_term, na=False)
        ]
        translated_results = pd.concat([translated_results, match])

    translated_results = translated_results.drop_duplicates()
    translated_results = translated_results.loc[
        ~translated_results.index.isin(exact_results.index)
        & ~translated_results.index.isin(partial_results.index)
    ]

    # ====== FUNCTION TO DISPLAY RESULTS WITH PDF PREVIEW ======
    import base64


    def show_results(title, results):
        st.markdown("---")
        st.subheader(f"{title} ({len(results)})")

        if not results.empty:
            for _, row in results.iterrows():
                file_name = row["file name"]
                pdf_path = Path(PDF_DIR) / file_name
                st.markdown(f"**📄 File:** {file_name}")

                if pdf_path.exists():
                    with st.expander("👁️ Preview PDF", expanded=False):
                        # Read PDF safely and display inline
                        with open(pdf_path, "rb") as f:
                            pdf_bytes = f.read()
                            base64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")

                        # Show download button
                        st.download_button(
                            label="⬇️ Download PDF",
                            data=pdf_bytes,
                            file_name=file_name,
                            mime="application/pdf",
                        )

                        # Show preview inline (offline-safe)
                        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="900" height="700" type="application/pdf"></iframe>'
                        st.markdown(pdf_display, unsafe_allow_html=True)
                else:
                    st.warning("⚠️ PDF file not found in the directory.")
        else:
            st.caption("No results found.")

    # ===== DISPLAY ALL THREE SECTIONS =====
    show_results("🎯 Exact Matches", exact_results)
    show_results("🔍 Partial Matches", partial_results)
    st.markdown("---")
    st.subheader(f"🌐 Translated Matches ({len(translated_results)})")
    if translated_terms:
        st.caption(f"Translated keywords: {', '.join(sorted(translated_terms))}")
    show_results("", translated_results)

else:
    st.info("Type a keyword above to search your artworks.")
