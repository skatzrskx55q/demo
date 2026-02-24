import os
import hmac
import streamlit as st

def check_password():
    expected = os.getenv("APP_PASSWORD")
    if not expected:
        st.error("APP_PASSWORD не задан в окружении.")
        return False

    if st.session_state.get("password_correct", False):
        return True

    def password_entered():
        entered = st.session_state.get("password", "")
        ok = hmac.compare_digest(entered, expected)
        st.session_state["password_correct"] = ok
        if ok:
            st.session_state.pop("password", None)

    st.text_input("Пароль", type="password", key="password", on_change=password_entered)

    if "password_correct" in st.session_state and not st.session_state["password_correct"]:
        st.error("Неверный пароль")

    return False

if not check_password():
    st.stop()


import json

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
        ],
        "loader": load_unified_excels,
        "loader_kwargs": {
            # Пример точечного override:
            # "parse_profile": {"filter": {"split_newline": False}},
        },
        "renderer": render_agreements_ui,
    },
    "Интенты": {
        "urls": [
            "https://raw.githubusercontent.com/skatzrskx55q/Retrieve2/main/intents22.xlsx",
        ],
        "loader": load_unified_excels,
        "loader_kwargs": {},
        "renderer": render_intents_ui,
    },
    "Generals": {
        "urls": [
            "https://raw.githubusercontent.com/skatzrskx55q/Retrieve2/main/intents33.xlsx",
        ],
        "loader": load_unified_excels,
        "loader_kwargs": {},
        "renderer": render_generals_ui,
    },
    "Confluence": {
        "urls": [
            "https://skatzr.atlassian.net/wiki/spaces/~7120203b1cf4260fea434db9c78c6e8549bd2b/pages/4194305",
        ],
        "loader": load_document_data,
        "loader_kwargs": {},
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


@st.cache_resource(ttl=3600)
def get_data(domain_name, loader_kwargs_key=""):
    _ = loader_kwargs_key  # Учитываем конфиг загрузки в ключе кэша.
    conf = DOCUMENTS[domain_name]
    loader_kwargs = conf.get("loader_kwargs") or {}
    return conf["loader"](conf["urls"], **loader_kwargs)


if domain:
    loader_kwargs = DOCUMENTS[domain].get("loader_kwargs") or {}
    loader_kwargs_key = json.dumps(loader_kwargs, sort_keys=True, ensure_ascii=False)
    df = get_data(domain, loader_kwargs_key=loader_kwargs_key)
    DOCUMENTS[domain]["renderer"](df)
