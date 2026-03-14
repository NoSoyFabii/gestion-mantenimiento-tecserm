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
            
            /* Limpieza de interfaz */
            header, footer { visibility: hidden; }
            
            /* Estilo de la tarjeta principal */
            .main-login-box {
                background: #161b22;
                padding: 30px;
                border-radius: 15px;
                border: 1px solid #30363d;
                box-shadow: 0 10px 30px rgba(0,0,0,0.5);
                text-align: center;
            }

            /* RECUADRO SUPERIOR NEÓN */
            .neon-header {
                border: 2px solid #00d4ff;
                padding: 15px;
                border-radius: 10px;
                box-shadow: 0 0 15px rgba(0, 212, 255, 0.3);
                margin-bottom: 20px;
            }

            .title-main {
                font-family: 'Orbitron', sans-serif;
                color: #00d4ff;
                font-size: 24px;
                font-weight: 900;
                margin: 0;
            }

            .subtitle-main {
                font-family: 'Rajdhani', sans-serif;
                color: #00ff87;
                font-size: 14px;
                font-weight: 700;
                text-transform: uppercase;
                margin: 5px 0 0 0;
            }

            /* Etiquetas de texto técnico */
            .label-tech {
                font-family: 'Rajdhani', sans-serif;
                color: #8b949e;
                font-size: 12px;
                font-weight: 700;
                text-align: left;
                text-transform: uppercase;
                margin-top: 15px;
            }

            /* Botón de acceso */
            .stButton>button {
                background: #00d4ff !important;
                color: #0d1117 !important;
                font-family: 'Orbitron', sans-serif !important;
                font-weight: 900 !important;
                border: none !important;
                padding: 12px !important;
                margin-top: 25px !important;
                box-shadow: 0 4px 15px rgba(0, 212, 255, 0.3) !important;
            }
            </style>
        """, unsafe_allow_html=True)

        # Usamos columnas para el centrado horizontal
        _, col, _ = st.columns([0.6, 1, 0.6])
        
        with col:
            st.markdown("<br><br>", unsafe_allow_html=True) # Espacio para bajarlo un poco
            
            # Recuadro Superior Neón
            st.markdown("""
                <div class="neon-header">
                    <p class="title-main">TECSERM S.A.C</p>
                    <p class="subtitle-main">Sistema de control de vehiculos</p>
                </div>
            """, unsafe_allow_html=True)

            # Logo mediano (Usamos st.image directamente para evitar fallos)
            if os.path.exists("logo.png"):
                st.image("logo.png", width=180) 
            
            # Formulario
            st.markdown('<p class="label-tech">Identificación de Usuario</p>', unsafe_allow_html=True)
            user = st.text_input("User", label_visibility="collapsed", placeholder="Ingrese su ID")
            
            st.markdown('<p class="label-tech">Clave de Seguridad</p>', unsafe_allow_html=True)
            password = st.text_input("Pass", type="password", label_visibility="collapsed", placeholder="••••••••")
            
            if st.button("ACCEDER AL SISTEMA", use_container_width=True):
                if user in USUARIOS and USUARIOS[user] == password:
                    st.session_state.autenticado = True
                    st.rerun()
                else:
                    st.error("Credenciales incorrectas")

        st.stop()