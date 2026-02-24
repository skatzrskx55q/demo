import html

import streamlit as st

from utils import semantic_search_document


def render(df):
    query = st.text_input("Введите запрос по документу:")

    if query:
        try:
            results = semantic_search_document(query, df)
            if results:
                st.markdown("### 📄 Релевантные фрагменты")
                for score, chunk in results:
                    st.markdown(
                        f"""
                    <div style="border:1px solid #e0e0e0;border-radius:12px;padding:16px;margin-bottom:16px;background-color:#f9f9f9;box-shadow:0 2px 6px rgba(0,0,0,0.05);">
                        <div style="font-size:13px;color:#888;">Релевантность: {score:.2f}</div>
                        <div style="margin-top:8px; white-space: pre-wrap;">{html.escape(chunk)}</div>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )
            else:
                st.info("Ничего не найдено.")
        except Exception as e:
            st.error(f"Ошибка: {e}")
