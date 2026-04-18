from __future__ import annotations

import streamlit as st


def require_password() -> None:
    if st.session_state.get("authed"):
        return

    st.title("📋 Daily List")
    pw = st.text_input("Password", type="password", key="pw_input")
    if st.button("Enter"):
        if pw == st.secrets["app_password"]:
            st.session_state["authed"] = True
            st.rerun()
        else:
            st.error("Nope.")
    st.stop()
