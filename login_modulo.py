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

        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Rajdhani:wght@500;700&display=swap');

        .stApp{
            background: radial-gradient(circle at top,#0d1b2a,#020617);
        }

        header, footer, #MainMenu{
            visibility:hidden;
        }

        .block-container{
            padding-top:6vh;
            display:flex;
            justify-content:center;
        }

        .login-card{
            width:520px;
            background:#0f172a;
            padding:45px;
            border-radius:18px;
            border:1px solid #1f2937;
            box-shadow:0 30px 60px rgba(0,0,0,0.6);
            text-align:center;
        }

        .login-title{
            font-family:'Orbitron';
            font-size:38px;
            font-weight:900;
            color:#00e5ff;
        }

        .login-sub{
            font-family:'Rajdhani';
            font-size:18px;
            color:#00ff9c;
            margin-bottom:25px;
        }

        .input-label{
            text-align:left;
            font-family:'Rajdhani';
            color:#94a3b8;
            font-weight:700;
            margin-top:15px;
        }

        .input-icon{
            margin-right:8px;
            color:#00e5ff;
        }

        .stTextInput input{
            background:#020617;
            border:1px solid #334155;
            border-radius:10px;
            padding:12px;
            color:white;
        }

        .stButton>button{
            background:linear-gradient(90deg,#00e5ff,#0066ff);
            border:none;
            font-family:'Orbitron';
            font-weight:700;
            height:50px;
            border-radius:12px;
            margin-top:25px;
            color:white;
            transition:0.3s;
        }

        .stButton>button:hover{
            transform:scale(1.03);
            box-shadow:0 0 15px #00e5ff;
        }

        .logo-center img{
            margin:auto;
            display:block;
            margin-bottom:10px;
        }

        </style>
        """, unsafe_allow_html=True)


        st.markdown('<div class="login-card">', unsafe_allow_html=True)

        st.markdown("""
        <div class="login-title">
        INICIAR SESIÓN
        </div>

        <div class="login-sub">
        SISTEMA DE CONTROL VEHICULAR
        </div>
        """, unsafe_allow_html=True)

        if os.path.exists("logo.png"):
            st.markdown('<div class="logo-center">', unsafe_allow_html=True)
            st.image("logo.png", width=170)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="input-label"><i class="fa-solid fa-user input-icon"></i>Usuario</div>', unsafe_allow_html=True)
        user = st.text_input("", placeholder="Ingrese su ID de acceso", label_visibility="collapsed")

        st.markdown('<div class="input-label"><i class="fa-solid fa-lock input-icon"></i>Contraseña</div>', unsafe_allow_html=True)
        password = st.text_input("", type="password", placeholder="Ingrese su contraseña", label_visibility="collapsed")

        if st.button("ACCEDER AL SISTEMA", use_container_width=True):

            if user in USUARIOS and USUARIOS[user] == password:
                st.session_state.autenticado = True
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos")

        st.markdown("</div>", unsafe_allow_html=True)

        st.stop()