import streamlit as st
import os

USUARIOS = {"admin": "tecserm2026", "logistica": "log2026"}

def check_login():
    if "autenticado" not in st.session_state:
        st.session_state.autenticado = False

    if not st.session_state.autenticado:
        # CSS para diseño vivo, compacto y sin scroll
        st.markdown("""
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&family=Rajdhani:wght@600&display=swap');
            
            /* Eliminar scroll y márgenes extra */
            .main { overflow: hidden; }
            .block-container { padding-top: 2rem !important; }
            
            /* Contenedor principal con borde neón */
            .login-card {
                background: linear-gradient(145deg, #0d1117, #161b22);
                padding: 30px;
                border-radius: 15px;
                border: 2px solid #00d4ff;
                box-shadow: 0 0 20px rgba(0, 212, 255, 0.3);
                text-align: center;
            }

            .stTextInput font { color: #00d4ff !important; }
            
            /* Título vibrante */
            .vibrant-title {
                font-family: 'Orbitron', sans-serif;
                background: linear-gradient(90deg, #00d4ff, #00ff87);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                font-size: 26px;
                font-weight: 900;
                margin-bottom: 5px;
                text-shadow: 2px 2px 10px rgba(0, 212, 255, 0.5);
            }

            /* Botón Neón */
            .stButton>button {
                background: linear-gradient(90deg, #0072ff, #00d4ff) !important;
                color: white !important;
                border: none !important;
                font-family: 'Orbitron', sans-serif !important;
                font-weight: bold !important;
                box-shadow: 0 4px 15px rgba(0, 114, 255, 0.4) !important;
                transition: 0.3s !important;
            }
            .stButton>button:hover {
                transform: scale(1.02);
                box-shadow: 0 4px 20px rgba(0, 212, 255, 0.6) !important;
            }
            </style>
        """, unsafe_allow_html=True)

        # Layout centrado y compacto
        _, col, _ = st.columns([0.8, 1, 0.8])
        
        with col:
            # Contenedor visual
            with st.container():
                # Logo más pequeño y centrado
                if os.path.exists("logo.png"):
                    sub_c1, sub_c2, sub_c3 = st.columns([1, 1.2, 1])
                    with sub_c2:
                        st.image("logo.png", width=140) # Tamaño reducido
                
                st.markdown('<p class="vibrant-title">TECSERM 2026</p>', unsafe_allow_html=True)
                st.markdown("<p style='color: #00ff87; font-family: Rajdhani; font-size: 14px; margin-bottom: 20px;'>SISTEMA DE CONTROL DE ACTIVOS</p>", unsafe_allow_html=True)
                
                # Formulario
                user = st.text_input("USUARIO", placeholder="👤 ID de empleado")
                password = st.text_input("CONTRASEÑA", type="password", placeholder="🔑 ••••••••")
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                if st.button("ACCESO SEGURO", use_container_width=True):
                    if user in USUARIOS and USUARIOS[user] == password:
                        st.session_state.autenticado = True
                        st.rerun()
                    else:
                        st.error("Acceso Denegado")

        st.stop()