import streamlit as st

from ui.agreements_ui import render as render_agreements_ui
from ui.generals_ui import render as render_generals_ui
from ui.intents_ui import render as render_intents_ui
from ui.rag_ui import render as render_rag_ui
from utils import (
    load_unified_excels,
    load_document_data,
)

st.set_page_config(page_title="Проверка фраз", layout="centered")
st.title("🤖 Проверка фраз")

DOCUMENTS = {
    "Договорённости": {
        "urls": [
            "https://raw.githubusercontent.com/skatzrskx55q/Retrieve2/main/data66.xlsx",
            "https://raw.githubusercontent.com/skatzrsk/semantic-assistant/main/data21.xlsx",
            "https://raw.githubusercontent.com/skatzrsk/semantic-assistant/main/data31.xlsx",
        ],
        "loader": lambda urls: load_unified_excels(urls),
        "renderer": render_agreements_ui,
    },
    "Интенты": {
        "urls": [
            "https://raw.githubusercontent.com/skatzrskx55q/Retrieve2/main/intents22.xlsx",
        ],
        "loader": lambda urls: load_unified_excels(urls),
        "renderer": render_intents_ui,
    },
    "Generals": {
        "urls": [
            "https://raw.githubusercontent.com/skatzrskx55q/Retrieve2/main/intents33.xlsx",
        ],
        "loader": lambda urls: load_unified_excels(urls),
        "renderer": render_generals_ui,
    },
    "Confluence": {
        "urls": [
            "https://skatzr.atlassian.net/wiki/spaces/~7120203b1cf4260fea434db9c78c6e8549bd2b/pages/4194305",
        ],
        "loader": lambda urls: load_document_data(urls),
        "renderer": render_rag_ui,
    },
}

TEAMS = {
    "Чат-бот": ["Confluence"],
    "Голос": ["Договорённости", "Интенты", "Generals"],
    "Чат-Бот2": [],
    "Чат-Бот3": [],
}

with st.sidebar:
    st.header("Выбор команды")
    team = st.radio("Команда", options=list(TEAMS.keys()), index=1)
    team_docs = TEAMS[team]
    st.header("Выбор документа")
    if team_docs:
        domain = st.radio("Документ", options=team_docs, index=0)
    else:
        domain = None
        st.info("Для этой команды документы пока не настроены.")


@st.cache_data(ttl=3600)
def get_data(domain_name):
    conf = DOCUMENTS[domain_name]
    return conf["loader"](conf["urls"])


if domain:
    df = get_data(domain)
    DOCUMENTS[domain]["renderer"](df)
