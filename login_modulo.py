# login_modulo.py
import streamlit as st
import os

USUARIOS = {"admin": "tecserm2026", "logistica": "log2026"}

def check_login():
    if "autenticado" not in st.session_state:
        st.session_state.autenticado = False

    if not st.session_state.autenticado:
        _, col, _ = st.columns([1, 0.8, 1])
        with col:
            st.markdown("<br><br>", unsafe_allow_html=True)
            st.markdown('<div style="background:#161b22; padding:30px; border-radius:15px; border:1px solid #30363d; text-align:center; color:white;">', unsafe_allow_html=True)
            if os.path.exists("logo.png"):
                st.image("logo.png", width=180)
            st.subheader("Acceso TECSERM 2026")
            user = st.text_input("Usuario")
            password = st.text_input("Contraseña", type="password")
            if st.button("INGRESAR", use_container_width=True):
                if user in USUARIOS and USUARIOS[user] == password:
                    st.session_state.autenticado = True
                    st.rerun()
                else:
                    st.error("Credenciales incorrectas")
            st.markdown('</div>', unsafe_allow_html=True)
        st.stop() # Bloquea el resto del código si no hay login