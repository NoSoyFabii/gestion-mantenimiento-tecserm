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
            
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            footer {visibility: hidden;}
            
            /* TRUCO PARA CENTRADO PERFECTO EN PANTALLA COMPLETA */
            div[data-testid="stVerticalBlock"] > div {
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                min-height: 85vh; /* Centrado vertical con respecto a la altura de vista */
            }

            .stForm {
                border: none !important;
                padding: 0px !important;
                background-color: transparent !important;
            }

            /* Contenedor principal estilo Glassmorphism */
            .login-card {
                background: #161b22;
                padding: 40px;
                border-radius: 15px;
                border: 1px solid #30363d;
                box-shadow: 0 10px 30px rgba(0,0,0,0.6);
                text-align: center;
                max-width: 450px; /* Ancho máximo para que no se estire mucho */
                width: 100%;
            }

            /* RECUADRO SUPERIOR NEÓN CON TEXTOS DENTRO */
            .info-box-neon {
                border: 2px solid #00d4ff;
                padding: 15px;
                border-radius: 8px;
                box-shadow: 0 0 15px rgba(0, 212, 255, 0.4);
                margin-bottom: 25px;
                text-align: center;
            }

            .company-name {
                font-family: 'Orbitron', sans-serif;
                color: #00d4ff;
                font-size: 26px;
                font-weight: 900;
                margin-bottom: 3px;
                letter-spacing: 1px;
            }
            
            .system-name {
                font-family: 'Rajdhani', sans-serif;
                color: #00ff87; /* Verde brillante */
                font-size: 14px;
                font-weight: 700;
                letter-spacing: 2px;
                text-transform: uppercase;
                margin: 0px;
            }

            /* Estilo para etiquetas técnicas */
            .label-tech {
                font-family: 'Rajdhani', sans-serif;
                color: #8b949e;
                font-size: 13px;
                font-weight: 700;
                margin-bottom: 5px;
                text-align: left;
                text-transform: uppercase;
            }

            /* Botón Cian Neón */
            .stButton>button {
                background: #00d4ff !important;
                color: #0d1117 !important;
                font-family: 'Orbitron', sans-serif !important;
                font-weight: 900 !important;
                font-size: 16px !important;
                border: none !important;
                padding: 12px !important;
                margin-top: 20px !important;
                letter-spacing: 1px !important;
                transition: 0.3s !important;
            }
            .stButton>button:hover {
                transform: scale(1.02);
                box-shadow: 0 0 20px rgba(0, 212, 255, 0.6) !important;
            }
            </style>
        """, unsafe_allow_html=True)

        with st.container():
            # El div que envuelve todo para el CSS de centrado
            st.markdown('<div class="login-card">', unsafe_allow_html=True)
            
            # Recuadro Superior Neón con Textos
            st.markdown("""
                <div class="info-box-neon">
                    <p class="company-name">TECSERM S.A.C</p>
                    <p class="system-name">Sistema de control de vehiculos</p>
                </div>
            """, unsafe_allow_html=True)
            
            # Logo (Mediano y centrado)
            if os.path.exists("logo.png"):
                lc1, lc2, lc3 = st.columns([1, 1.8, 1])
                with lc2:
                    st.image("logo.png", use_container_width=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Campos de entrada
            with st.form("credenciales"):
                st.markdown('<p class="label-tech">Identificación de Usuario</p>', unsafe_allow_html=True)
                user = st.text_input("Usuario", label_visibility="collapsed", placeholder="Ingrese su ID")
                
                st.markdown('<p class="label-tech">Clave de Seguridad</p>', unsafe_allow_html=True)
                password = st.text_input("Contraseña", type="password", label_visibility="collapsed", placeholder="••••••••")
                
                if st.form_submit_button("ACCEDER"):
                    if user in USUARIOS and USUARIOS[user] == password:
                        st.session_state.autenticado = True
                        st.rerun()
                    else:
                        st.error("Credenciales incorrectas")
            
            st.markdown('</div>', unsafe_allow_html=True)

        st.stop()