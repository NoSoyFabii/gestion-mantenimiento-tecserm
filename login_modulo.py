import streamlit as st
import os

st.set_page_config(page_title="Sistema Vehicular", layout="wide")

USUARIOS = {"admin": "tecserm2026", "logistica": "log2026"}

def check_login():

    if "autenticado" not in st.session_state:
        st.session_state.autenticado = False

    if not st.session_state.autenticado:

        st.markdown("""
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">

        <style>

        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600;800&family=Rajdhani:wght@500;700&display=swap');

        header, footer, #MainMenu {visibility:hidden;}

        /* FONDO */
        .stApp{
            background: radial-gradient(circle at center,#081426,#020617);
        }

        /* TARJETA */
        .login-card{
            width:360px;
            background:#0b1220;
            padding:40px;
            border-radius:18px;
            border:1px solid #1f2937;
            box-shadow:0 30px 60px rgba(0,0,0,0.6);
            text-align:center;
        }

        /* TITULO */
        .title{
            font-family:'Orbitron';
            font-size:42px;
            font-weight:800;
            color:#00e5ff;
            margin-bottom:5px;
        }

        /* SUBTITULO */
        .subtitle{
            font-family:'Rajdhani';
            font-size:20px;
            color:#00ff9c;
            margin-bottom:25px;
        }

        /* LABELS */
        .label{
            text-align:left;
            font-family:'Rajdhani';
            color:#9ca3af;
            font-weight:700;
            margin-top:12px;
        }

        .icon{
            margin-right:6px;
            color:#00e5ff;
        }

        /* INPUTS */
        .stTextInput input{
            background:#020617;
            border:1px solid #334155;
            border-radius:10px;
            padding:12px;
            color:white;
        }

        /* BOTON */
        .stButton>button{
            background:linear-gradient(90deg,#00e5ff,#0066ff);
            border:none;
            font-family:'Orbitron';
            font-weight:700;
            height:46px;
            border-radius:10px;
            margin-top:20px;
            color:white;
            transition:0.3s;
        }

        .stButton>button:hover{
            transform:scale(1.05);
            box-shadow:0 0 18px #00e5ff;
        }

        </style>
        """, unsafe_allow_html=True)

        # COLUMNAS PARA CENTRAR
        col1, col2, col3 = st.columns([1,1,1])

        with col2:

            st.markdown('<div class="login-card">', unsafe_allow_html=True)

            st.markdown('<div class="title">INICIAR SESIÓN</div>', unsafe_allow_html=True)
            st.markdown('<div class="subtitle">SISTEMA DE CONTROL VEHICULAR</div>', unsafe_allow_html=True)

            if os.path.exists("logo.png"):
                st.image("logo.png", width=120)

            st.markdown('<div class="label"><i class="fa-solid fa-user icon"></i>Usuario</div>', unsafe_allow_html=True)
            user = st.text_input("", placeholder="Ingrese su ID", label_visibility="collapsed")

            st.markdown('<div class="label"><i class="fa-solid fa-lock icon"></i>Contraseña</div>', unsafe_allow_html=True)
            password = st.text_input("", type="password", placeholder="Ingrese su contraseña", label_visibility="collapsed")

            if st.button("ACCEDER AL SISTEMA", use_container_width=True):

                if user in USUARIOS and USUARIOS[user] == password:
                    st.session_state.autenticado = True
                    st.rerun()
                else:
                    st.error("Usuario o contraseña incorrectos")

            st.markdown("</div>", unsafe_allow_html=True)

        st.stop()