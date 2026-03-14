import streamlit as st
import os

USUARIOS = {"admin": "tecserm2026", "logistica": "log2026"}

def check_login():
    if "autenticado" not in st.session_state:
        st.session_state.autenticado = False

    if not st.session_state.autenticado:
        # 1. Centramos todo con columnas (ajustamos pesos para que sea más ancho en móvil)
        _, col, _ = st.columns([0.5, 1.2, 0.5])
        
        with col:
            # Espacio superior para bajar el formulario
            st.markdown("<br><br>", unsafe_allow_html=True)
            
            # Contenedor con estilo para el formulario
            with st.container(border=True):
                # Centrado del LOGO
                if os.path.exists("logo.png"):
                    # Usamos HTML para forzar el centrado perfecto y tamaño
                    st.markdown(
                        """
                        <div style="display: flex; justify-content: center; margin-bottom: 10px;">
                            <img src="app/static/logo.png" width="220">
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )
                    # Nota: Si el HTML de arriba no carga la imagen, usa esta línea de abajo:
                    # st.image("logo.png", width=250)
                
                st.markdown("<h2 style='text-align: center; color: white; font-family: sans-serif;'>Acceso TECSERM 2026</h2>", unsafe_allow_html=True)
                st.markdown("<p style='text-align: center; color: #8b949e;'>Ingrese sus credenciales para continuar</p>", unsafe_allow_html=True)
                st.markdown("---")

                # Inputs
                user = st.text_input("👤 Usuario", placeholder="Ej: admin")
                password = st.text_input("🔑 Contraseña", type="password", placeholder="••••••••")
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Botón llamativo
                if st.button("🔓 INGRESAR AL SISTEMA", use_container_width=True, type="primary"):
                    if user in USUARIOS and USUARIOS[user] == password:
                        st.session_state.autenticado = True
                        st.rerun()
                    else:
                        st.error("❌ Usuario o contraseña incorrectos")

        # Detiene el resto de la app
        st.stop()