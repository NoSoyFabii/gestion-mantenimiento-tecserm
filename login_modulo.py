import streamlit as st
import os

USUARIOS = {"admin": "tecserm2026", "logistica": "log2026"}

def check_login():
    if "autenticado" not in st.session_state:
        st.session_state.autenticado = False

    if not st.session_state.autenticado:
        st.markdown("""
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&family=Rajdhani:wght@500;700&display=swap');
            
            /* Fondo y limpieza de interfaz */
            .stApp { background-color: #0d1117; }
            header, footer { visibility: hidden; }
            
            /* Tarjeta de Login Mediana */
            .login-card {
                background: #161b22;
                padding: 40px;
                border-radius: 12px;
                border: 2px solid #00d4ff;
                box-shadow: 0 0 25px rgba(0, 212, 255, 0.2);
                margin-top: 20px;
            }

            /* Títulos vibrantes */
            .company-name {
                font-family: 'Orbitron', sans-serif;
                color: #00d4ff;
                font-size: 28px;
                font-weight: 900;
                text-align: center;
                margin-bottom: 0px;
                letter-spacing: 1px;
            }
            .system-name {
                font-family: 'Rajdhani', sans-serif;
                color: #00ff87;
                font-size: 16px;
                font-weight: 700;
                text-align: center;
                margin-bottom: 25px;
                letter-spacing: 3px;
                text-transform: uppercase;
            }

            /* Estilo para etiquetas de texto sin emojis */
            .label-tech {
                font-family: 'Rajdhani', sans-serif;
                color: #8b949e;
                font-size: 13px;
                font-weight: 700;
                margin-bottom: 5px;
                text-transform: uppercase;
            }

            /* Botón de alto contraste */
            .stButton>button {
                background: #00d4ff !important;
                color: #0d1117 !important;
                font-family: 'Orbitron', sans-serif !important;
                font-weight: 900 !important;
                border: none !important;
                padding: 10px !important;
                margin-top: 15px !important;
            }
            </style>
        """, unsafe_allow_html=True)

        # Layout centrado
        _, col, _ = st.columns([0.7, 1.1, 0.7])
        
        with col:
            st.markdown('<div class="login-card">', unsafe_allow_html=True)
            
            # Logo Mediano
            if os.path.exists("logo.png"):
                lc1, lc2, lc3 = st.columns([1, 1.5, 1])
                with lc2:
                    st.image("logo.png", width=180) # Tamaño mediano corregido
            
            st.markdown('<p class="company-name">TECSERM S.A.C</p>', unsafe_allow_html=True)
            st.markdown('<p class="system-name">Sistema de control de vehiculos</p>', unsafe_allow_html=True)
            
            # Campos de entrada limpios (sin emojis)
            st.markdown('<p class="label-tech">Identificación de Usuario</p>', unsafe_allow_html=True)
            user = st.text_input("Usuario", label_visibility="collapsed", placeholder="ID de acceso")
            
            st.markdown('<p class="label-tech">Clave de Seguridad</p>', unsafe_allow_html=True)
            password = st.text_input("Contraseña", type="password", label_visibility="collapsed", placeholder="••••••••")
            
            if st.button("ACCEDER", use_container_width=True):
                if user in USUARIOS and USUARIOS[user] == password:
                    st.session_state.autenticado = True
                    st.rerun()
                else:
                    st.error("Credenciales incorrectas")
            
            st.markdown('</div>', unsafe_allow_html=True)

        st.stop()