import streamlit as st
import pandas as pd
import os
import time
from datetime import datetime
from streamlit_option_menu import option_menu
import io
from supabase import create_client, Client

# --- 1. CONFIGURACIÓN DE PÁGINA ---
if os.path.exists("logo.png"):
    st.set_page_config(page_title="TECSERM S.A.C 2026", page_icon="logo.png", layout="wide")
else:
    st.set_page_config(page_title="TECSERM S.A.C 2026", page_icon="🚛", layout="wide")

# --- 2. CONEXIÓN A SUPABASE (Lógica corregida) ---
try:
    SUPABASE_URL = st.secrets["connections"]["supabase"]["url"]
    SUPABASE_KEY = st.secrets["connections"]["supabase"]["key"]
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    st.error(f"Error crítico de conexión: {e}")
    supabase = None

def ejecutar_query(query_str=None, params=(), fetch=False, tabla="vehiculos"):
    try:
        if fetch:
            res = supabase.table(tabla).select("*").execute()
            return pd.DataFrame(res.data)
        
        if query_str and "INSERT INTO vehiculos" in query_str:
            data = {
                "codigo_tcs": params[0], "placa": params[1], "marca": params[2],
                "frecuencia": int(params[3]), "km_ultimo_manto": int(params[4]), "km_actual": int(params[5])
            }
            supabase.table(tabla).insert(data).execute()
            
        elif query_str and "UPDATE vehiculos SET km_actual" in query_str:
            supabase.table(tabla).update({"km_actual": int(params[0])}).eq("codigo_tcs", params[1]).execute()
            
        elif query_str and "UPDATE vehiculos SET km_ultimo_manto" in query_str:
            # Esta es tu lógica original de reinicio de ciclo
            supabase.table(tabla).update({
                "km_ultimo_manto": int(params[0]), 
                "km_actual": int(params[1])
            }).eq("codigo_tcs", params[2]).execute()
            
        elif query_str and "DELETE FROM vehiculos" in query_str:
            supabase.table(tabla).delete().eq("codigo_tcs", params[0]).execute()
            
        st.cache_data.clear()
        return True
    except Exception as e:
        st.error(f"Error en base de datos: {e}")
        return False

def registrar_historial(codigo, accion, km, lugar="N/A"):
    try:
        fecha_hoy = datetime.now().strftime("%d/%m/%Y %H:%M")
        data = {
            "fecha": fecha_hoy, "codigo_tcs": str(codigo), 
            "accion": accion, "kilometraje": int(km), "lugar": lugar
        }
        supabase.table("historial").insert(data).execute()
    except Exception as e:
        st.error(f"Error al guardar historial: {e}")

# --- 3. DISEÑO CSS (MEJORADO PARA MÓVIL Y ESTÉTICA) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&family=Rajdhani:wght@600;700&display=swap');
    
    /* Ocultar flecha de sidebar en móviles */
    button[kind="header"] { display: none !important; }
    
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
    
    /* Evitar saltos de layout en móvil */
    .block-container { padding-top: 2rem !important; }
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

# --- 5. VISTAS (Lógica original completa) ---

if selected == "Panel Control":
    st.subheader("📊 Monitoreo de Unidades")
    df = ejecutar_query(fetch=True, tabla="vehiculos")
    if not df.empty:
        df['Recorrido'] = df['km_actual'].astype(int) - df['km_ultimo_manto'].astype(int)
        df['% Uso'] = ((df['Recorrido'] / df['frecuencia'].astype(int)) * 100).clip(0, 110)

        for index, row in df.iterrows():
            p = row['% Uso']
            color_hex = "#3fb950" if p < 60 else "#d29922" if p < 85 else "#f85149"
            u_id = f"unit_{row['codigo_tcs']}".replace("-", "_")
            st.markdown(f"""
            <div id="{u_id}">
                <div class="card" style="border: 2px solid {color_hex}66; box-shadow: 0px 4px 10px {color_hex}11; margin-bottom: 10px;">
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
    df_v = ejecutar_query(fetch=True, tabla="vehiculos")
    if not df_v.empty:
        u_sel = st.selectbox("Seleccione Unidad", df_v['codigo_tcs'])
        val_actual = int(df_v[df_v['codigo_tcs'] == u_sel]['km_actual'].values[0])
        with st.form("form_registro_semanal"):
            c1, c2 = st.columns(2)
            nuevo_km = c1.number_input(f"KM Actual", min_value=val_actual, value=val_actual, step=1)
            lugar = c2.text_input("Lugar / Ubicación actual", placeholder="Ej: Moquegua, Taller Ilo...")
            if st.form_submit_button("💾 GUARDAR REPORTE"):
                ejecutar_query("UPDATE vehiculos SET km_actual", (nuevo_km, u_sel))
                registrar_historial(u_sel, "ACTUALIZACIÓN KM", nuevo_km, lugar)
                st.success(f"✅ Reporte guardado")
                st.balloons()
                time.sleep(1.5)
                st.rerun()

elif selected == "Mantenimiento":
    st.subheader("🔧 Reiniciar Ciclo")
    df_v = ejecutar_query(fetch=True, tabla="vehiculos")
    if not df_v.empty:
        u_m = st.selectbox("Unidad que recibió servicio", df_v['codigo_tcs'])
        with st.form("manto_fix"):
            c1, c2 = st.columns(2)
            km_serv = c1.number_input("KM exacto del servicio", min_value=0, step=1)
            lugar_m = c2.text_input("Taller / Lugar de Mantenimiento", placeholder="Ej: Soluciones Hidráulicas")
            if st.form_submit_button("⚙️ REINICIAR CONTADOR"):
                # Mantenemos tu lógica de 3 parámetros para el UPDATE de mantenimiento
                ejecutar_query("UPDATE vehiculos SET km_ultimo_manto", (km_serv, km_serv, u_m))
                registrar_historial(u_m, "MANTENIMIENTO REALIZADO", km_serv, lugar_m)
                st.success(f"✅ Ciclo reiniciado correctamente.")
                st.balloons()
                time.sleep(2) 
                st.rerun()

elif selected == "Historial":
    st.subheader("🕒 Expediente Individual")
    df_v = ejecutar_query(fetch=True, tabla="vehiculos")
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
        hist = ejecutar_query(fetch=True, tabla="historial")
        if not hist.empty:
            hist_filtrado = hist[hist['codigo_tcs'] == u_busq].sort_values(by="fecha", ascending=False)
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
            df_raw = ejecutar_query(fetch=True)
            if not df_raw.empty:
                df_raw['Prox. Manto'] = df_raw['km_ultimo_manto'].astype(int) + df_raw['frecuencia'].astype(int)
                df_raw['KM Faltantes'] = df_raw['Prox. Manto'] - df_raw['km_actual'].astype(int)
                df_raw['Estado'] = df_raw['KM Faltantes'].apply(lambda x: 'CRÍTICO' if x < 200 else ('ALERTA' if x < 600 else 'OPERATIVO'))
                
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    df_raw.to_excel(writer, index=False, sheet_name='Reporte', startrow=5)
                    workbook  = writer.book
                    worksheet = writer.sheets['Reporte']
                    
                    # FORMATO CORPORATIVO FULL
                    header_fmt = workbook.add_format({'bold': True, 'bg_color': '#1f6feb', 'font_color': 'white', 'border': 1, 'align': 'center', 'valign': 'vcenter'})
                    title_fmt = workbook.add_format({'bold': True, 'font_size': 16, 'font_color': '#1f6feb', 'align': 'center', 'valign': 'vcenter'})
                    data_fmt = workbook.add_format({'border': 1, 'align': 'center'})
                    
                    worksheet.merge_range('C1:G2', 'SISTEMA DE GESTIÓN DE MANTENIMIENTO - TECSERM S.A.C', title_fmt)
                    worksheet.write('C3', f'Fecha de Reporte: {datetime.now().strftime("%d/%m/%Y")}')
                    
                    for col_num, value in enumerate(df_raw.columns.values):
                        worksheet.write(5, col_num, value, header_fmt)
                        worksheet.set_column(col_num, col_num, 15)

                st.download_button(label="⬇️ Descargar Excel", data=output.getvalue(), file_name=f"Reporte_TECSERM_{datetime.now().strftime('%Y%m%d')}.xlsx")

    with c2:
        st.markdown("### Gestión de Datos")
        df_del = ejecutar_query(fetch=True)
        if not df_del.empty:
            target = st.selectbox("Eliminar Unidad:", df_del['codigo_tcs'])
            if st.button("❌ ELIMINAR", type="primary"):
                ejecutar_query("DELETE FROM vehiculos", (target,))
                st.success("Unidad eliminada.")
                time.sleep(1.2)
                st.rerun()

st.markdown("---")
st.caption("TECSERM S.A.C © 2026 - FABIOLAPP:)")