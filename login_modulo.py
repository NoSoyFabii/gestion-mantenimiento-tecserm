import streamlit as st
import os

# Credenciales de acceso
USUARIOS = {"admin": "tecserm2026", "logistica": "log2026"}

def check_login():
    if "autenticado" not in st.session_state:
        st.session_state.autenticado = False

    if not st.session_state.autenticado:
        st.markdown("""
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&family=Rajdhani:wght@600;700&display=swap');
            
            /* Ocultar elementos nativos de Streamlit */
            header, footer, #MainMenu { visibility: hidden; }
            
            /* Fondo oscuro profundo */
            .stApp { 
                background-color: #0d1117; 
                display: flex;
                justify-content: center;
                align-items: center;
            }

            /* Contenedor principal centrado */
            .login-container {
                display: flex;
                justify-content: center;
                align-items: center;
                width: 100%;
                min-height: 100vh;
            }

            /* Tarjeta de Login estilo Industrial */
            .login-card {
                background: #161b22;
                padding: 40px;
                border-radius: 20px;
                border: 1px solid #30363d;
                box-shadow: 0 25px 50px rgba(0,0,0,0.6);
                width: 450px;
                text-align: center;
                margin: auto;
            }

            /* Recuadro Superior Neón */
            .neon-header-box {
                border: 3px solid #00d4ff;
                border-radius: 12px;
                padding: 20px;
                margin-bottom: 30px;
                box-shadow: 0 0 20px rgba(0, 212, 255, 0.3);
                background: rgba(0, 212, 255, 0.02);
            }

            .company-title {
                font-family: 'Orbitron', sans-serif;
                color: #00d4ff;
                font-size: 34px; /* Texto grande */
                font-weight: 900;
                margin: 0;
                letter-spacing: 1px;
            }

            .system-subtitle {
                font-family: 'Rajdhani', sans-serif;
                color: #00ff87;
                font-size: 18px; /* Texto mediano-grande */
                font-weight: 700;
                text-transform: uppercase;
                margin-top: 10px;
                letter-spacing: 2px;
            }

            /* Estilo de etiquetas (labels) */
            .label-modern {
                font-family: 'Rajdhani', sans-serif;
                color: #8b949e;
                font-size: 14px;
                font-weight: 700;
                text-align: left;
                text-transform: uppercase;
                margin-top: 20px;
                display: block;
            }

            /* Botón Cian Neón */
            .stButton>button {
                background: linear-gradient(90deg, #00d4ff, #0072ff) !important;
                color: white !important;
                font-family: 'Orbitron', sans-serif !important;
                font-weight: 900 !important;
                font-size: 18px !important;
                border: none !important;
                border-radius: 8px !important;
                padding: 12px !important;
                margin-top: 30px !important;
                box-shadow: 0 5px 15px rgba(0, 212, 255, 0.4) !important;
                transition: 0.3s;
            }

            .stButton>button:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 25px rgba(0, 212, 255, 0.6) !important;
            }

            /* Inputs centrados visualmente */
            .stTextInput>div>div>input {
                background-color: #0d1117 !important;
                color: white !important;
                border: 1px solid #30363d !important;
            }
            </style>
        """, unsafe_allow_html=True)

        # Usamos columnas solo para ayudar al centrado horizontal de Streamlit
        _, center_col, _ = st.columns([0.1, 1, 0.1])
        
        with center_col:
            # Todo dentro de un div con la clase login-card
            st.markdown('<div class="login-card">', unsafe_allow_html=True)
            
            # Recuadro Neón
            st.markdown("""
                <div class="neon-header-box">
                    <p class="company-title">TECSERM S.A.C</p>
                    <p class="system-subtitle">Sistema de Control de Vehículos</p>
                </div>
            """, unsafe_allow_html=True)

            # Logo Grandecito (220px)
            if os.path.exists("logo.png"):
                st.image("logo.png", width=220)
            
            # Formulario sin etiquetas nativas para usar las personalizadas
            st.markdown('<span class="label-modern">Identificación de Usuario</span>', unsafe_allow_html=True)
            user = st.text_input("User", label_visibility="collapsed", placeholder="Usuario")
            
            st.markdown('<span class="label-modern">Clave de Seguridad</span>', unsafe_allow_html=True)
            password = st.text_input("Pass", type="password", label_visibility="collapsed", placeholder="••••••••")
            
            if st.button("ACCEDER AL PANEL", use_container_width=True):
                if user in USUARIOS and USUARIOS[user] == password:
                    st.session_state.autenticado = True
                    st.rerun()
                else:
                    st.error("Credenciales no autorizadas")
            
            st.markdown('</div>', unsafe_allow_html=True)

        st.stop()