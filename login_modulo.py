import streamlit as st
import os

USUARIOS = {"admin": "tecserm2026", "logistica": "log2026"}

def check_login():
    if "autenticado" not in st.session_state:
        st.session_state.autenticado = False

    if not st.session_state.autenticado:
        st.markdown("""
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&family=Rajdhani:wght@600;700&display=swap');
            
            /* Fondo y limpieza */
            .stApp { background-color: #0d1117; }
            header, footer, #MainMenu { visibility: hidden; }

            /* CENTRADO CRÍTICO */
            [data-testid="stVerticalBlock"] {
                align-items: center !important;
                justify-content: center !important;
            }

            /* TARJETA ANGOSTA (Como al principio pero mejorada) */
            .login-card {
                background: #161b22;
                padding: 30px;
                border-radius: 20px;
                border: 1px solid #30363d;
                box-shadow: 0 20px 50px rgba(0,0,0,0.5);
                width: 480px; /* Ancho angosto y elegante */
                text-align: center;
                margin: auto;
            }

            /* RECUADRO NEÓN CON LETRAS GRANDES QUE SE AJUSTAN */
            .neon-header-box {
                border: 3px solid #00d4ff;
                border-radius: 12px;
                padding: 15px; /* Menos padding para dar espacio a la letra */
                margin-bottom: 25px;
                box-shadow: 0 0 20px rgba(0, 212, 255, 0.3);
                background: rgba(0, 212, 255, 0.05);
            }

            .company-title {
                font-family: 'Orbitron', sans-serif;
                color: #00d4ff;
                /* Tamaño grande que se adapta al ancho del cuadro */
                font-size: 42px; 
                font-weight: 900;
                margin: 0;
                text-align: center;
                line-height: 1;
                letter-spacing: -1px;
            }

            .system-subtitle {
                font-family: 'Rajdhani', sans-serif;
                color: #00ff87;
                font-size: 20px;
                font-weight: 700;
                text-transform: uppercase;
                margin-top: 8px;
                text-align: center;
                letter-spacing: 1px;
            }

            /* Etiquetas y Logo */
            .label-tech {
                font-family: 'Rajdhani', sans-serif;
                color: #8b949e;
                font-size: 14px;
                text-transform: uppercase;
                margin-top: 15px;
                margin-bottom: 5px;
                font-weight: 700;
                text-align: center;
            }

            .stImage > img {
                display: block;
                margin: 0 auto;
            }

            /* Botón */
            .stButton>button {
                background: linear-gradient(90deg, #00d4ff, #0072ff) !important;
                color: white !important;
                font-family: 'Orbitron', sans-serif !important;
                font-weight: 900 !important;
                border: none !important;
                margin-top: 25px !important;
                height: 50px;
            }
            </style>
        """, unsafe_allow_html=True)

        # Contenedor principal
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        
        # Recuadro Superior
        st.markdown("""
            <div class="neon-header-box">
                <p class="company-title">TECSERM S.A.C</p>
                <p class="system-subtitle">CONTROL DE VEHÍCULOS</p>
            </div>
        """, unsafe_allow_html=True)

        # Logo centrado (Tamaño mediano para que quepa bien)
        if os.path.exists("logo.png"):
            st.image("logo.png", width=200)
        
        # Inputs centrados
        st.markdown('<p class="label-tech">Usuario</p>', unsafe_allow_html=True)
        user = st.text_input("User", label_visibility="collapsed", placeholder="ID de acceso")
        
        st.markdown('<p class="label-tech">Contraseña</p>', unsafe_allow_html=True)
        password = st.text_input("Pass", type="password", label_visibility="collapsed", placeholder="••••••••")
        
        if st.button("ACCEDER AL PANEL", use_container_width=True):
            if user in USUARIOS and USUARIOS[user] == password:
                st.session_state.autenticado = True
                st.rerun()
            else:
                st.error("Credenciales no válidas")
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.stop()