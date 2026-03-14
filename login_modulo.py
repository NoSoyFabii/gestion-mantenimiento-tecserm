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
            
            /* 1. FONDO DIFUMINADO ANIMADO */
            .stApp {
                background: linear-gradient(-45deg, #0f172a, #1e1b4b, #2e1065, #1e1b4b);
                background-size: 400% 400%;
                animation: gradient 15s ease infinite;
            }
            @keyframes gradient {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }

            /* 2. FORZAR CENTRADO ABSOLUTO */
            [data-testid="stVerticalBlock"] {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
            }

            /* 3. TARJETA MODERNA (Glassmorphism) */
            .glass-card {
                background: rgba(255, 255, 255, 0.05);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                padding: 40px;
                width: 400px;
                box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
                text-align: center;
            }

            /* 4. RECUADRO SUPERIOR MODERNO */
            .neon-border-box {
                border: 2px solid #00d4ff;
                border-radius: 12px;
                padding: 15px;
                margin-bottom: 25px;
                background: rgba(0, 212, 255, 0.05);
            }

            .title-text {
                font-family: 'Orbitron', sans-serif;
                color: #00d4ff;
                font-size: 24px;
                font-weight: 900;
                margin: 0;
                text-shadow: 0 0 10px rgba(0, 212, 255, 0.5);
            }

            .subtitle-text {
                font-family: 'Rajdhani', sans-serif;
                color: #34d399; /* Verde esmeralda */
                font-size: 14px;
                font-weight: 700;
                letter-spacing: 2px;
                margin-top: 5px;
            }

            /* 5. INPUTS Y BOTÓN */
            .label-modern {
                font-family: 'Rajdhani', sans-serif;
                color: #94a3b8;
                font-size: 12px;
                text-align: left;
                text-transform: uppercase;
                margin-top: 15px;
                width: 100%;
            }

            .stButton>button {
                background: linear-gradient(90deg, #00d4ff, #0072ff) !important;
                color: white !important;
                border: none !important;
                border-radius: 10px !important;
                font-family: 'Orbitron', sans-serif !important;
                font-weight: bold !important;
                height: 45px !important;
                margin-top: 30px !important;
                transition: 0.3s !important;
            }
            
            .stButton>button:hover {
                box-shadow: 0 0 20px rgba(0, 212, 255, 0.6) !important;
                transform: translateY(-2px);
            }

            header, footer { visibility: hidden; }
            </style>
        """, unsafe_allow_html=True)

        # Contenedor para agrupar todo
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        
        # Recuadro con textos
        st.markdown("""
            <div class="neon-border-box">
                <p class="title-text">TECSERM S.A.C</p>
                <p class="subtitle-text">Sistema de control de vehiculos</p>
            </div>
        """, unsafe_allow_html=True)

        # Logo mediano
        if os.path.exists("logo.png"):
            st.image("logo.png", width=160)

        # Entradas (sin emojis, estilo limpio)
        st.markdown('<p class="label-modern">Identificación de Usuario</p>', unsafe_allow_html=True)
        user = st.text_input("User", label_visibility="collapsed", placeholder="Username")
        
        st.markdown('<p class="label-modern">Clave de Seguridad</p>', unsafe_allow_html=True)
        password = st.text_input("Pass", type="password", label_visibility="collapsed", placeholder="••••••••")
        
        if st.button("INGRESAR AL PANEL", use_container_width=True):
            if user in USUARIOS and USUARIOS[user] == password:
                st.session_state.autenticado = True
                st.rerun()
            else:
                st.error("Credenciales no válidas")
        
        st.markdown('</div>', unsafe_allow_html=True)

        st.stop()