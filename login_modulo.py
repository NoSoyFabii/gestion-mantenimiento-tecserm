import streamlit as st
import os

USUARIOS = {"logistica": "log2026"}

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
                display: flex;
                flex-direction: column;
            }

            /* 3. Tarjeta de Login - ANCHO AMPLIADO para letras gigantes */
            .login-card {
                background: #161b22;
                padding: 50px;
                border-radius: 25px;
                border: 1px solid #30363d;
                box-shadow: 0 20px 60px rgba(0,0,0,0.6);
                width: 900px; /* Aumentado para que el texto de 100px quepa */
                text-align: center;
                display: flex;
                flex-direction: column;
                align-items: center;
                margin: auto;
            }

            /* 4. Recuadro Neón Superior */
            .neon-header-box {
                border: 4px solid #00d4ff;
                border-radius: 15px;
                padding: 30px;
                margin-bottom: 35px;
                box-shadow: 0 0 25px rgba(0, 212, 255, 0.4);
                background: rgba(0, 212, 255, 0.05);
                width: 100%;
                box-sizing: border-box;
            }

            .company-title {
                font-family: 'Orbitron', sans-serif;
                color: #00d4ff;
                font-size: 100px; /* TAMAÑO SOLICITADO */
                font-weight: 900;
                margin: 0;
                text-align: center;
                line-height: 1;
                white-space: nowrap; /* Evita que se rompa en dos líneas */
            }

            .system-subtitle {
                font-family: 'Rajdhani', sans-serif;
                color: #00ff87;
                font-size: 70px; /* Ajustado de 80 a 70 para legibilidad técnica */
                font-weight: 700;
                text-transform: uppercase;
                margin-top: 15px;
                text-align: center;
                letter-spacing: 3px;
                line-height: 1;
            }

            /* 5. Etiquetas de entrada */
            .label-modern {
                font-family: 'Rajdhani', sans-serif;
                color: #8b949e;
                font-size: 20px;
                font-weight: 700;
                text-transform: uppercase;
                margin-top: 30px;
                margin-bottom: 10px;
                text-align: center;
                width: 100%;
            }

            /* 6. Botón */
            .stButton>button {
                background: linear-gradient(90deg, #00d4ff, #0072ff) !important;
                color: white !important;
                font-family: 'Orbitron', sans-serif !important;
                font-weight: 900 !important;
                font-size: 24px !important;
                border: none !important;
                border-radius: 12px !important;
                padding: 20px !important;
                margin-top: 40px !important;
                width: 100% !important;
                box-shadow: 0 8px 20px rgba(0, 212, 255, 0.4) !important;
            }

            /* Centrado forzado de logo */
            .stImage {
                display: flex;
                justify-content: center;
                margin: 20px 0;
            }
            </style>
        """, unsafe_allow_html=True)

        # Inicio de la tarjeta
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        
        # 1. Recuadro con textos
        st.markdown("""
            <div class="neon-header-box">
                <p class="company-title">TECSERM S.A.C</p>
                <p class="system-subtitle">CONTROL DE VEHÍCULOS</p>
            </div>
        """, unsafe_allow_html=True)

        # 2. Logo Centrado (Aumentado a 300 para que no se pierda con las letras)
        if os.path.exists("logo.png"):
            st.image("logo.png", width=300)
        
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
        
        st.markdown('</div>', unsafe_allow_html=True) # Cierre de la tarjeta
        st.stop()