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
            
            /* 1. Fondo y ocultar elementos nativos */
            .stApp { background-color: #0d1117; }
            header, footer, #MainMenu { visibility: hidden; }

            /* 2. Forzar centrado de la columna de Streamlit */
            [data-testid="stVerticalBlock"] {
                align-items: center !important;
                justify-content: center !important;
            }

            /* 3. Tarjeta de Login (Ancho controlado) */
            .login-card {
                background: #161b22;
                padding: 40px;
                border-radius: 20px;
                border: 1px solid #30363d;
                box-shadow: 0 20px 50px rgba(0,0,0,0.5);
                width: 500px; /* Ancho fijo para que no se estire */
                text-align: center;
                display: flex;
                flex-direction: column;
                align-items: center;
            }

            /* 4. Recuadro Neón Superior con Texto Centrado y Grande */
            .neon-header-box {
                border: 3px solid #00d4ff;
                border-radius: 12px;
                padding: 25px;
                margin-bottom: 30px;
                box-shadow: 0 0 20px rgba(0, 212, 255, 0.3);
                background: rgba(0, 212, 255, 0.05);
                width: 100%; /* Ocupa el ancho de la tarjeta */
                box-sizing: border-box;
            }

            .company-title {
                font-family: 'Orbitron', sans-serif;
                color: #00d4ff;
                font-size: 38px; /* ¡Más grande! */
                font-weight: 900;
                margin: 0;
                text-align: center;
            }

            .system-subtitle {
                font-family: 'Rajdhani', sans-serif;
                color: #00ff87;
                font-size: 20px; /* ¡Más grande! */
                font-weight: 700;
                text-transform: uppercase;
                margin-top: 10px;
                text-align: center;
                letter-spacing: 2px;
            }

            /* 5. Etiquetas de entrada centradas */
            .label-modern {
                font-family: 'Rajdhani', sans-serif;
                color: #8b949e;
                font-size: 15px;
                font-weight: 700;
                text-transform: uppercase;
                margin-top: 20px;
                margin-bottom: 8px;
                text-align: center;
                width: 100%;
            }

            /* 6. Botón centrado y llamativo */
            .stButton>button {
                background: linear-gradient(90deg, #00d4ff, #0072ff) !important;
                color: white !important;
                font-family: 'Orbitron', sans-serif !important;
                font-weight: 900 !important;
                font-size: 20px !important;
                border: none !important;
                border-radius: 10px !important;
                padding: 15px !important;
                margin-top: 35px !important;
                width: 100% !important;
                box-shadow: 0 5px 15px rgba(0, 212, 255, 0.4) !important;
            }
            
            /* Ajuste para que la imagen siempre esté al centro */
            .stImage > img {
                display: block;
                margin-left: auto;
                margin-right: auto;
            }
            </style>
        """, unsafe_allow_html=True)

        # Contenedor para agrupar y centrar todo
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        
        # 1. Recuadro con textos (Centrados y Grandes)
        st.markdown("""
            <div class="neon-header-box">
                <p class="company-title">TECSERM S.A.C</p>
                <p class="system-subtitle">Sistema de Control de Vehículos</p>
            </div>
        """, unsafe_allow_html=True)

        # 2. Logo Centrado y Grande
        if os.path.exists("logo.png"):
            st.image("logo.png", width=250)
        
        # 3. Entradas de Usuario
        st.markdown('<p class="label-modern">Identificación de Usuario</p>', unsafe_allow_html=True)
        user = st.text_input("User", label_visibility="collapsed", placeholder="ID de acceso")
        
        st.markdown('<p class="label-modern">Clave de Seguridad</p>', unsafe_allow_html=True)
        password = st.text_input("Pass", type="password", label_visibility="collapsed", placeholder="••••••••")
        
        # 4. Botón de acceso
        if st.button("ACCEDER AL PANEL", use_container_width=True):
            if user in USUARIOS and USUARIOS[user] == password:
                st.session_state.autenticado = True
                st.rerun()
            else:
                st.error("Credenciales no válidas")
        
        st.markdown('</div>', unsafe_allow_html=True)

        st.stop()