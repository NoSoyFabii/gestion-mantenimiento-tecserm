import streamlit as st
import os

USUARIOS = {"admin": "tecserm2026", "logistica": "log2026"}

def check_login():
    if "autenticado" not in st.session_state:
        st.session_state.autenticado = False

    if not st.session_state.autenticado:
        # Configuración de página ancha para evitar que Streamlit comprima la letra
        st.markdown("""
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&family=Rajdhani:wght@600;700&display=swap');
            
            /* 1. ELIMINAR LÍMITES DE ANCHO DE STREAMLIT */
            .block-container {
                max-width: 100% !important;
                padding: 0 !important;
            }
            .stApp { background-color: #0d1117; }
            header, footer, #MainMenu { visibility: hidden; }

            /* 2. CENTRADO TOTAL DEL CONTENIDO */
            [data-testid="stVerticalBlock"] {
                align-items: center !important;
                justify-content: center !important;
                min-height: 100vh;
                display: flex;
            }

            /* 3. TARJETA DE LOGIN - MUY ANCHA */
            .login-card {
                background: #161b22;
                padding: 60px;
                border-radius: 30px;
                border: 2px solid #30363d;
                box-shadow: 0 30px 70px rgba(0,0,0,0.8);
                width: 1100px; /* Ancho suficiente para letras de 100px */
                text-align: center;
                display: flex;
                flex-direction: column;
                align-items: center;
            }

            /* 4. RECUADRO CON LETRAS GIGANTES */
            .neon-header-box {
                border: 5px solid #00d4ff;
                border-radius: 20px;
                padding: 40px;
                margin-bottom: 40px;
                box-shadow: 0 0 30px rgba(0, 212, 255, 0.4);
                background: rgba(0, 212, 255, 0.05);
                width: 100%;
            }

            .company-title {
                font-family: 'Orbitron', sans-serif;
                color: #00d4ff;
                font-size: 110px; /* ¡SUPER GIGANTE! */
                font-weight: 900;
                margin: 0;
                text-align: center;
                line-height: 1;
                white-space: nowrap; 
                text-shadow: 0 0 20px rgba(0, 212, 255, 0.6);
            }

            .system-subtitle {
                font-family: 'Rajdhani', sans-serif;
                color: #00ff87;
                font-size: 60px; /* Subtítulo muy grande */
                font-weight: 700;
                text-transform: uppercase;
                margin-top: 20px;
                text-align: center;
                letter-spacing: 5px;
            }

            /* Etiquetas de los inputs */
            .label-modern {
                font-family: 'Rajdhani', sans-serif;
                color: #8b949e;
                font-size: 24px;
                font-weight: 700;
                text-transform: uppercase;
                margin-top: 30px;
                width: 100%;
                text-align: center;
            }

            /* Botón de acceso */
            .stButton>button {
                background: linear-gradient(90deg, #00d4ff, #0072ff) !important;
                color: white !important;
                font-family: 'Orbitron', sans-serif !important;
                font-weight: 900 !important;
                font-size: 28px !important;
                border-radius: 15px !important;
                padding: 25px !important;
                margin-top: 50px !important;
                width: 100% !important;
                box-shadow: 0 10px 30px rgba(0, 212, 255, 0.5) !important;
            }

            /* Centrado de logo */
            [data-testid="stImage"] {
                display: flex;
                justify-content: center;
            }
            </style>
        """, unsafe_allow_html=True)

      
        
        # Recuadro con textos
        st.markdown("""
            <div class="neon-header-box">
                <p class="company-title">TECSERM S.A.C</p>
                <p class="system-subtitle">CONTROL DE VEHÍCULOS</p>
            </div>
        """, unsafe_allow_html=True)

        # Logo Centrado
        if os.path.exists("logo.png"):
            st.image("logo.png", width=350)
        
        # Inputs (Crecieron también para que no se vean raros)
        st.markdown('<p class="label-modern">Usuario</p>', unsafe_allow_html=True)
        user = st.text_input("User", label_visibility="collapsed")
        
        st.markdown('<p class="label-modern">Contraseña</p>', unsafe_allow_html=True)
        password = st.text_input("Pass", type="password", label_visibility="collapsed")
        
        if st.button("INGRESAR AL SISTEMA", use_container_width=True):
            if user in USUARIOS and USUARIOS[user] == password:
                st.session_state.autenticado = True
                st.rerun()
            else:
                st.error("Credenciales Incorrectas")
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.stop()