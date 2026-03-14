import streamlit as st
import os

st.set_page_config(page_title="Sistema de Control Vehicular", layout="centered")

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

        .stApp{
            background: radial-gradient(circle at top,#071426,#020617);
        }

        /* CONTENEDOR CENTRADO */
        .block-container{
            display:flex;
            justify-content:center;
            padding-top:8vh;
        }

        /* TARJETA ANGOSTA */
        .login-card{
            width:380px;
            background:#0b1220;
            padding:40px;
            border-radius:18px;
            border:1px solid #1f2937;
            box-shadow:0 25px 60px rgba(0,0,0,0.6);
            text-align:center;
        }

        /* TITULO */
        .login-title{
            font-family:'Orbitron';
            font-size:44px;
            font-weight:800;
            color:#00e5ff;
            margin-bottom:5px;
        }

        /* SUBTITULO */
        .login-sub{
            font-family:'Rajdhani';
            font-size:20px;
            color:#00ff9c;
            margin-bottom:30px;
            letter-spacing:1px;
        }

        /* LOGO */
        .logo img{
            margin:auto;
            display:block;
            margin-bottom:15px;
        }

        /* LABEL */
        .input-label{
            text-align:left;
            font-family:'Rajdhani';
            color:#94a3b8;
            font-weight:700;
            margin-top:15px;
        }

        .icon{
            margin-right:8px;
            color:#00e5ff;
        }

        /* INPUT */
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
            height:48px;
            border-radius:10px;
            margin-top:25px;
            color:white;
            transition:0.3s;
        }

        .stButton>button:hover{
            transform:scale(1.05);
            box-shadow:0 0 18px #00e5ff;
        }

        </style>
        """, unsafe_allow_html=True)


        st.markdown('<div class="login-card">', unsafe_allow_html=True)

        st.markdown("""
        <div class="login-title">INICIAR SESIÓN</div>
        <div class="login-sub">SISTEMA DE CONTROL VEHICULAR</div>
        """, unsafe_allow_html=True)

        if os.path.exists("logo.png"):
            st.markdown('<div class="logo">', unsafe_allow_html=True)
            st.image("logo.png", width=130)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="input-label"><i class="fa-solid fa-user icon"></i>Usuario</div>', unsafe_allow_html=True)
        user = st.text_input("", placeholder="Ingrese su ID de acceso", label_visibility="collapsed")

        st.markdown('<div class="input-label"><i class="fa-solid fa-lock icon"></i>Contraseña</div>', unsafe_allow_html=True)
        password = st.text_input("", type="password", placeholder="Ingrese su contraseña", label_visibility="collapsed")

        if st.button("ACCEDER AL SISTEMA", use_container_width=True):

            if user in USUARIOS and USUARIOS[user] == password:
                st.session_state.autenticado = True
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos")

        st.markdown("</div>", unsafe_allow_html=True)

        st.stop()