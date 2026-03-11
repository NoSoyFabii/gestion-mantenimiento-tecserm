import streamlit as st
import pandas as pd
import os
import time
from datetime import datetime
from streamlit_option_menu import option_menu
import io
from streamlit_gsheets import GSheetsConnection

# --- 1. CONFIGURACIÓN DE PÁGINA ---
if os.path.exists("logo.png"):
    st.set_page_config(page_title="TECSERM S.A.C 2026", page_icon="logo.png", layout="wide")
else:
    st.set_page_config(page_title="TECSERM S.A.C 2026", page_icon="🚛", layout="wide")

# --- 2. CONEXIÓN A GOOGLE SHEETS (REEMPLAZA A SQLITE) ---
conn = st.connection("gsheets", type=GSheetsConnection)

def ejecutar_query(query_str, params=(), fetch=False, tabla="vehiculos"):
    try:
        # Intentamos leer la hoja de cálculo
        df = conn.read(worksheet=tabla, ttl="0")
    except Exception as e:
        # Si la hoja está vacía o no se puede leer, creamos un DataFrame vacío con las columnas correctas
        if tabla == "vehiculos":
            df = pd.DataFrame(columns=["codigo_tcs", "placa", "marca", "frecuencia", "km_ultimo_manto", "km_actual"])
        else:
            df = pd.DataFrame(columns=["fecha", "codigo_tcs", "accion", "kilometraje", "lugar"])
    
    if fetch:
        return df
    
    try:
        # Simulación de lógica SQL para Google Sheets
        if query_str and "INSERT INTO vehiculos" in query_str:
            nueva_fila = pd.DataFrame([{
                "codigo_tcs": params[0], "placa": params[1], "marca": params[2],
                "frecuencia": params[3], "km_ultimo_manto": params[4], "km_actual": params[5]
            }])
            df = pd.concat([df, nueva_fila], ignore_index=True)
            
        elif query_str and "UPDATE vehiculos SET km_actual" in query_str:
            df['codigo_tcs'] = df['codigo_tcs'].astype(str)
            df.loc[df['codigo_tcs'] == str(params[1]), 'km_actual'] = params[0]
            
        elif query_str and "UPDATE vehiculos SET km_ultimo_manto" in query_str:
            df['codigo_tcs'] = df['codigo_tcs'].astype(str)
            df.loc[df['codigo_tcs'] == str(params[2]), ['km_ultimo_manto', 'km_actual']] = params[0]
            
        elif query_str and "DELETE FROM vehiculos" in query_str:
            df['codigo_tcs'] = df['codigo_tcs'].astype(str)
            df = df[df['codigo_tcs'] != str(params[0])]
        
        # Guardar cambios en la nube
        conn.update(worksheet=tabla, data=df)
        st.cache_data.clear()
        return True
    except Exception as e:
        st.error(f"Error al actualizar datos: {e}")
        return False

def registrar_historial(codigo, accion, km, lugar="N/A"):
    try:
        fecha_hoy = datetime.now().strftime("%d/%m/%Y %H:%M")
        try:
            df_h = conn.read(worksheet="historial", ttl="0")
        except:
            df_h = pd.DataFrame(columns=["fecha", "codigo_tcs", "accion", "kilometraje", "lugar"])
            
        nueva_fila = pd.DataFrame([{
            "fecha": fecha_hoy, 
            "codigo_tcs": str(codigo), 
            "accion": accion, 
            "kilometraje": km, 
            "lugar": lugar
        }])
        df_h = pd.concat([df_h, nueva_fila], ignore_index=True)
        conn.update(worksheet=tabla="historial", data=df_h)
    except Exception as e:
        st.error(f"Error en historial: {e}")

# --- 3. DISEÑO CSS (TU DISEÑO ORIGINAL) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&family=Rajdhani:wght@600;700&display=swap');
    .main-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 1.8rem !important;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(90deg, #1f6feb, #58a6ff, #1f6feb);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 4s linear infinite;
        margin-bottom: 25px;
    }
    @keyframes shine { to { background-position: 200% center; } }
    .card { background: rgba(255, 255, 255, 0.03); padding: 20px; border-radius: 15px; font-family: 'Rajdhani', sans-serif; }
    .km-badge { background-color: #161b22; padding: 4px 12px; border-radius: 8px; font-family: 'Orbitron', sans-serif; font-size: 12px; font-weight: bold; }
    h1, h2, h3, label, .stMarkdown { font-family: 'Rajdhani', sans-serif !important; }
    .stButton > button { width: 100%; border-radius: 8px; font-family: 'Orbitron', sans-serif; }
</style>
""", unsafe_allow_html=True)

# --- 4. BARRA LATERAL ---
with st.sidebar:
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)
    st.markdown('<div style="text-align:center; font-family:\'Orbitron\'; font-weight:bold; color:#58a6ff; letter-spacing:2px;">TECSERM S.A.C</div>', unsafe_allow_html=True)
    
    selected = option_menu(
        menu_title=None,
        options=["Panel Control", "Registrar KM", "Nueva Unidad", "Mantenimiento", "Historial", "Ajustes"],
        icons=["grid-fill", "speedometer", "plus-circle", "tools", "clock-history", "gear"],
        default_index=0,
        styles={
            "nav-link": {"font-family": "Rajdhani", "font-size": "18px", "text-align": "left"},
            "nav-link-selected": {"background-color": "#1f6feb"}
        }
    )

st.markdown('<div class="main-title">GESTIÓN DE MANTENIMIENTO PREVENTIVO</div>', unsafe_allow_html=True)

# --- 5. VISTAS ---

if selected == "Panel Control":
    st.subheader("📊 Monitoreo de Unidades")
    df = ejecutar_query("SELECT * FROM vehiculos", fetch=True)
    if not df.empty:
        df['Recorrido'] = df['km_actual'].astype(int) - df['km_ultimo_manto'].astype(int)
        df['% Uso'] = ((df['Recorrido'] / df['frecuencia'].astype(int)) * 100).clip(0, 110)

        for index, row in df.iterrows():
            p = row['% Uso']
            color_hex = "#3fb950" if p < 60 else "#d29922" if p < 85 else "#f85149"
            u_id = f"unit_{row['codigo_tcs']}".replace("-", "_")
            st.markdown(f"""
            <style>
                div[data-testid="stVerticalBlock"] > div:has(div#{u_id}) + div .stProgress > div > div > div > div {{
                    background-color: {color_hex} !important;
                }}
            </style>
            <div id="{u_id}">
                <div class="card" style="border: 2px solid {color_hex}66; box-shadow: 0px 4px 10px {color_hex}11;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <b style="font-size: 22px; font-family: 'Orbitron'; color: white;">{row['codigo_tcs']}</b>
                            <p style="margin:0; font-size:18px; color: #8b949e;">{row['placa']} | {row['marca']}</p>
                        </div>
                        <div style="text-align: right;">
                            <span class="km-badge" style="color: {color_hex}; border: 1px solid {color_hex}44;">KM ACTUAL: {int(row['km_actual']):,}</span>
                            <div style="color: {color_hex}; font-size: 24px; font-weight: 900; font-family: 'Orbitron'; margin-top:5px;">{p:.1f}%</div>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.progress(min(p/100, 1.0))
            st.markdown("<div style='margin-bottom:25px;'></div>", unsafe_allow_html=True)

elif selected == "Registrar KM":
    st.subheader("📝 Actualizar Kilometraje")
    df_v = ejecutar_query("SELECT * FROM vehiculos", fetch=True)
    if not df_v.empty:
        u_sel = st.selectbox("Seleccione Unidad", df_v['codigo_tcs'])
        val_actual = int(df_v[df_v['codigo_tcs'] == u_sel]['km_actual'].values[0])
        with st.form("form_registro_semanal"):
            c1, c2 = st.columns(2)
            nuevo_km = c1.number_input(f"KM Actual", min_value=val_actual, value=val_actual, step=1)
            lugar = c2.text_input("Lugar / Ubicación actual", placeholder="Ej: Moquegua, Taller Ilo, Mina...")
            if st.form_submit_button("💾 GUARDAR REPORTE"):
                ejecutar_query("UPDATE vehiculos SET km_actual", (nuevo_km, u_sel))
                registrar_historial(u_sel, "ACTUALIZACIÓN KM", nuevo_km, lugar)
                st.success(f"✅ Reporte guardado")
                st.balloons()
                time.sleep(1.5)
                st.rerun()

elif selected == "Mantenimiento":
    st.subheader("🔧 Reiniciar Ciclo")
    df_v = ejecutar_query("SELECT * FROM vehiculos", fetch=True)
    if not df_v.empty:
        u_m = st.selectbox("Unidad que recibió servicio", df_v['codigo_tcs'])
        with st.form("manto_fix"):
            c1, c2 = st.columns(2)
            km_serv = c1.number_input("KM exacto del servicio", min_value=0, step=1)
            lugar_m = c2.text_input("Taller / Lugar de Mantenimiento", placeholder="Ej: Soluciones Hidráulicas")
            if st.form_submit_button("⚙️ REINICIAR CONTADOR"):
                ejecutar_query("UPDATE vehiculos SET km_ultimo_manto", (km_serv, km_serv, u_m))
                registrar_historial(u_m, "MANTENIMIENTO REALIZADO", km_serv, lugar_m)
                st.success(f"✅ Ciclo reiniciado correctamente.")
                st.balloons()
                time.sleep(2) 
                st.rerun()

elif selected == "Historial":
    st.subheader("🕒 Expediente Individual")
    df_v = ejecutar_query("SELECT * FROM vehiculos", fetch=True)
    if not df_v.empty:
        u_busq = st.selectbox("🔍 Seleccionar Vehículo:", df_v['codigo_tcs'])
        u_sel = df_v[df_v['codigo_tcs'] == u_busq].iloc[0]
        prox_manto = int(u_sel['km_ultimo_manto']) + int(u_sel['frecuencia'])
        restante = prox_manto - int(u_sel['km_actual'])
        c1, c2, c3 = st.columns(3)
        c1.metric("Último Manto", f"{int(u_sel['km_ultimo_manto']):,} KM")
        c2.metric("KM ACTUAL", f"{int(u_sel['km_actual']):,} KM")
        c3.metric("Próximo Manto", f"{prox_manto:,} KM", delta=f"{restante:,} restantes")
        st.markdown("---")
        hist = ejecutar_query(None, fetch=True, tabla="historial")
        hist_filtrado = hist[hist['codigo_tcs'] == u_busq].sort_index(ascending=False)
        st.dataframe(hist_filtrado[['fecha', 'accion', 'kilometraje', 'lugar']], use_container_width=True, hide_index=True)

elif selected == "Nueva Unidad":
    st.subheader("🚚 Alta de Vehículo")
    with st.form("new_unit_form"):
        c1, c2 = st.columns(2)
        cod = c1.text_input("Código TCS (Ej: TCS-01)")
        pla = c1.text_input("Placa")
        mar = c2.text_input("Marca / Modelo")
        fre = c2.selectbox("Frecuencia (KM)", [5000, 7500, 10000])
        ini = c1.number_input("Kilometraje Inicial", min_value=0, step=1)
        if st.form_submit_button("REGISTRAR UNIDAD"):
            if cod and pla:
                ejecutar_query("INSERT INTO vehiculos", (cod, pla, mar, fre, ini, ini))
                registrar_historial(cod, "ALTA", ini, "Base Central")
                st.success("✅ Unidad agregada.")
                time.sleep(1.5)
                st.rerun()

elif selected == "Ajustes":
    st.subheader("⚙️ Configuración")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### Exportar Reporte Ejecutivo")
        if st.button("📊 GENERAR EXCEL CORPORATIVO"):
            df_raw = ejecutar_query(None, fetch=True)
            if not df_raw.empty:
                df_raw['Prox. Manto'] = df_raw['km_ultimo_manto'].astype(int) + df_raw['frecuencia'].astype(int)
                df_raw['KM Faltantes'] = df_raw['Prox. Manto'] - df_raw['km_actual'].astype(int)
                df_raw['Estado'] = df_raw['KM Faltantes'].apply(lambda x: 'CRÍTICO' if x < 200 else ('ALERTA' if x < 600 else 'OPERATIVO'))
                
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    df_raw.to_excel(writer, index=False, sheet_name='Reporte', startrow=5)
                    workbook  = writer.book
                    worksheet = writer.sheets['Reporte']
                    # ... (Tu misma lógica de formato Excel original se mantiene aquí) ...
                    header_fmt = workbook.add_format({'bold': True, 'bg_color': '#1f6feb', 'font_color': 'white', 'border': 1, 'align': 'center'})
                    title_fmt = workbook.add_format({'bold': True, 'font_size': 14, 'font_color': '#1f6feb', 'align': 'center'})
                    
                    worksheet.merge_range('C1:I2', 'SISTEMA DE GESTIÓN DE CALIDAD', title_fmt)
                    for col_num, value in enumerate(df_raw.columns.values):
                        worksheet.write(5, col_num, value, header_fmt)

                st.download_button(label="⬇️ Descargar Excel", data=output.getvalue(), file_name=f"Reporte_TECSERM.xlsx")

    with c2:
        st.markdown("### Gestión de Datos")
        df_del = ejecutar_query(None, fetch=True)
        if not df_del.empty:
            target = st.selectbox("Eliminar Unidad:", df_del['codigo_tcs'])
            if st.button("❌ ELIMINAR", type="primary"):
                ejecutar_query("DELETE FROM vehiculos", (target,))
                st.success("Unidad eliminada.")
                time.sleep(1.2)
                st.rerun()