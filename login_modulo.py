import streamlit as st
import os

USUARIOS = {"admin": "tecserm2026", "logistica": "log2026"}

def check_login():
    if "autenticado" not in st.session_state:
        st.session_state.autenticado = False

    if not st.session_state.autenticado:
        # Estilos CSS Avanzados para un look moderno
        st.markdown("""
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;600&display=swap');
            
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            footer {visibility: hidden;}
            
            .login-box {
                background-color: rgba(22, 27, 34, 0.8);
                padding: 40px;
                border-radius: 20px;
                border: 1px solid #30363d;
                box-shadow: 0 10px 25px rgba(0,0,0,0.5);
                text-align: center;
            }
            
            .login-title {
                font-family: 'Orbitron', sans-serif;
                color: #58a6ff;
                font-size: 24px;
                font-weight: 700;
                margin-top: 20px;
                letter-spacing: 2px;
                text-transform: uppercase;
            }
            
            .login-subtitle {
                font-family: 'Inter', sans-serif;
                color: #8b949e;
                font-size: 14px;
                margin-bottom: 30px;
            }
            </style>
        """, unsafe_allow_html=True)

        # Centrado vertical y horizontal
        _, col, _ = st.columns([0.6, 1, 0.6])
        
        with col:
            st.markdown("<br><br>", unsafe_allow_html=True)
            
            with st.container():
                # Centrado del LOGO (Método seguro)
                if os.path.exists("logo.png"):
                    # Usamos columnas internas para centrar la imagen nativa
                    c1, c2, c3 = st.columns([0.2, 1, 0.2])
                    with c2:
                        st.image("logo.png", use_container_width=True)
                
                st.markdown('<p class="login-title">TECSERM S.A.C</p>', unsafe_allow_html=True)
                st.markdown('<p class="login-subtitle">SISTEMA DE GESTIÓN DE MANTENIMIENTO</p>', unsafe_allow_html=True)
                
                # Campos de texto con diseño limpio
                user = st.text_input("USER ID", placeholder="Ingrese usuario")
                password = st.text_input("PASSWORD", type="password", placeholder="••••••••")
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Botón con estilo "Primary"
                if st.button("ACCEDER AL SISTEMA", use_container_width=True, type="primary"):
                    if user in USUARIOS and USUARIOS[user] == password:
                        st.session_state.autenticado = True
                        st.rerun()
                    else:
                        st.error("Credenciales no autorizadas")
            
            # Footer decorativo
            st.markdown(
                "<p style='text-align: center; color: #30363d; font-size: 10px; margin-top: 50px;'>"
                "&copy; 2026 TECSERM S.A.C | Seguridad de Datos de Activos</p>", 
                unsafe_allow_html=True
            )

        st.stop()