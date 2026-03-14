import streamlit as st
import pandas as pd
import os
import time
from datetime import datetime
from streamlit_option_menu import option_menu
import io
from supabase import create_client, Client
from login_modulo import check_login

def cerrar_sesion():
    # Limpia todo el estado de la sesión
    for key in st.session_state.keys():
        del st.session_state[key]
    
    
# --- 1. CONFIGURACIÓN DE PÁGINA ---
if os.path.exists("logo.png"):
    st.set_page_config(page_title="TECSERM S.A.C 2026", page_icon="logo.png", layout="wide")
else:
    st.set_page_config(page_title="TECSERM S.A.C 2026", page_icon="🚛", layout="wide")

# --- 2. CONEXIÓN A SUPABASE ---
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
            df_res = pd.DataFrame(res.data)
            # --- AJUSTE DE ORDENAMIENTO ---
            if not df_res.empty and 'codigo_tcs' in df_res.columns:
               
                df_res = df_res.sort_values(by='codigo_tcs', key=lambda col: col.str.extract('(\d+)')[0].astype(int))
            return df_res
        
        if "INSERT INTO vehiculos" in query_str:
            data = {
                "codigo_tcs": params[0], "placa": params[1], "marca": params[2],
                "frecuencia": int(params[3]), "km_ultimo_manto": int(params[4]), "km_actual": int(params[5])
            }
            supabase.table("vehiculos").insert(data).execute()
        elif "UPDATE vehiculos SET km_actual" in query_str:
            supabase.table("vehiculos").update({"km_actual": int(params[0])}).eq("codigo_tcs", params[1]).execute()
        elif "UPDATE vehiculos SET km_ultimo_manto" in query_str:
            supabase.table("vehiculos").update({
                "km_ultimo_manto": int(params[0]), "km_actual": int(params[1])
            }).eq("codigo_tcs", params[2]).execute()
        elif "DELETE FROM vehiculos" in query_str:
            supabase.table("vehiculos").delete().eq("codigo_tcs", params[0]).execute()
        
        st.cache_data.clear()
        return True
    except Exception as e:
        st.error(f"Error en base de datos: {e}")
        return False

def registrar_historial(codigo, accion, km, lugar="N/A"):
    try:
        fecha_hoy = datetime.now().strftime("%d/%m/%Y %H:%M")
        data = {"fecha": fecha_hoy, "codigo_tcs": str(codigo), "accion": accion, "kilometraje": int(km), "lugar": lugar}
        supabase.table("historial").insert(data).execute()
    except Exception as e:
        st.error(f"Error al guardar historial: {e}")

# --- 3. DISEÑO CSS ADAPTATIVO (CLARO/OSCURO) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@500;600;700&display=swap');
    
    /* Título con degradado que funciona en ambos modos */
    .main-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 2.2rem !important;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(90deg, #1f6feb, #58a6ff, #1f6feb);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 4s linear infinite;
        margin-bottom: 30px;
    }

    /* Tarjeta Adaptativa */
    .card { 
        background: var(--background-secondary-color); /* Color automático de Streamlit */
        padding: 24px; 
        border-radius: 12px; 
        font-family: 'Rajdhani', sans-serif;
        border: 1px solid rgba(128, 128, 128, 0.2);
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
        margin-bottom: 5px;
    }

    /* Forzar color de texto dentro de la tarjeta para que siempre sea visible */
    .card h2, .card b {
        color: var(--text-color);
        margin: 0;
    }

    /* Badges de KM (Fondo neutro para ambos modos) */
    .km-badge { 
        background-color: rgba(128, 128, 128, 0.15); 
        color: var(--text-color);
        padding: 6px 14px; 
        border-radius: 6px; 
        font-family: 'Orbitron', sans-serif; 
        font-size: 13px; 
        font-weight: bold;
        border: 1px solid rgba(128, 128, 128, 0.1);
    }

    /* Botones con estilo corporativo */
    .stButton > button {
        border-radius: 8px !important;
        font-family: 'Orbitron', sans-serif !important;
        transition: 0.3s !important;
    }

    /* Ajuste para que los labels se lean bien siempre */
    label, .stMarkdown p {
        font-family: 'Rajdhani', sans-serif !important;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# --- 4. BARRA LATERAL ---

with st.sidebar:
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)
    
    st.markdown('<div style="text-align:center; font-family:\'Orbitron\'; font-weight:bold; color:#58a6ff; letter-spacing:2px;"></div>', unsafe_allow_html=True)
    
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

    st.markdown("---")
    st.button("🚪 CERRAR SESIÓN", use_container_width=True, on_click=cerrar_sesion)

st.markdown('<div class="main-title">GESTIÓN DE MANTENIMIENTO PREVENTIVO</div>', unsafe_allow_html=True)

# --- 5. VISTAS ---

if selected == "Panel Control":
    st.subheader("📊 Monitoreo de Unidades")
    df = ejecutar_query(fetch=True)
    if not df.empty:
        df['Recorrido'] = df['km_actual'].astype(int) - df['km_ultimo_manto'].astype(int)
        df['% Uso'] = ((df['Recorrido'] / df['frecuencia'].astype(int)) * 100).clip(0, 110)

        for index, row in df.iterrows():
            p = row['% Uso']
            # Color dinámico mejorado
            color_hex = "#3fb950" if p < 65 else "#d29922" if p < 85 else "#f85149"
            u_id = f"unit_{row['codigo_tcs']}".replace("-", "_")
            
            km_ini_f = f"{int(row['km_ultimo_manto']):,}"
            km_act_f = f"{int(row['km_actual']):,}"

            st.markdown(f"""
            <div id="{u_id}" class="card">
                <div style="display: flex; justify-content: space-between; align-items: start;">
                    <div>
                        <span style="color: {color_hex}; font-size: 12px; font-weight: bold;">● UNIDAD ACTIVA</span>
                        <h2 style="margin: 0; color: white; font-family: 'Orbitron';">{row['codigo_tcs']}</h2>
                        <p style="color: #8b949e; font-size: 16px; margin-bottom: 15px;">{row['placa']} • {row['marca']}</p>
                    </div>
                    <div style="text-align: right;">
                        <div style="color: {color_hex}; font-size: 32px; font-weight: 900; font-family: 'Orbitron';">{p:.1f}%</div>
                        <div style="color: #8b949e; font-size: 12px;">VIDA ÚTIL DE ACEITE</div>
                    </div>
                </div>
                <div style="display: flex; gap: 10px; margin-bottom: 10px;">
                    <div class="km-badge" style="border-left: 3px solid #30363d;">INICIO: {km_ini_f} KM</div>
                    <div class="km-badge" style="border-left: 3px solid {color_hex};">ACTUAL: {km_act_f} KM</div>
                </div>
            </div>
            <style>
                div[data-testid="stVerticalBlock"] > div:has(div#{u_id}) + div .stProgress > div > div > div > div {{
                    background-color: {color_hex} !important;
                    height: 12px;
                }}
            </style>
            """, unsafe_allow_html=True)
            st.progress(min(p/100, 1.0))
            st.markdown("<br>", unsafe_allow_html=True)

elif selected == "Registrar KM":
    st.subheader("📝 Actualizar Kilometraje")
    df_v = ejecutar_query(fetch=True)
    if not df_v.empty:
        u_sel = st.selectbox("Seleccione Unidad", df_v['codigo_tcs'])
        val_actual = int(df_v[df_v['codigo_tcs'] == u_sel]['km_actual'].values[0])
        with st.form("form_registro_semanal"):
            c1, c2 = st.columns(2)
            nuevo_km = c1.number_input(f"KM Actual", min_value=val_actual, value=val_actual, step=1)
            lugar = c2.text_input("Lugar / Ubicación actual", placeholder="Ej: Moquegua...")
            if st.form_submit_button("💾 GUARDAR REPORTE"):
                ejecutar_query("UPDATE vehiculos SET km_actual", (nuevo_km, u_sel))
                registrar_historial(u_sel, "ACTUALIZACIÓN KM", nuevo_km, lugar)
                st.success(f"✅ Reporte guardado")
                st.balloons()
                time.sleep(1.5)
                st.rerun()

elif selected == "Mantenimiento":
    st.subheader("🔧 Reiniciar Ciclo")
    df_v = ejecutar_query(fetch=True)
    if not df_v.empty:
        u_m = st.selectbox("Unidad que recibió servicio", df_v['codigo_tcs'])
        with st.form("manto_fix"):
            c1, c2 = st.columns(2)
            km_serv = c1.number_input("KM exacto del servicio", min_value=0, step=1)
            lugar_m = c2.text_input("Taller / Lugar", placeholder="Ej: Soluciones Hidráulicas")
            if st.form_submit_button("⚙️ REINICIAR CONTADOR"):
                ejecutar_query("UPDATE vehiculos SET km_ultimo_manto", (km_serv, km_serv, u_m))
                registrar_historial(u_m, "MANTENIMIENTO REALIZADO", km_serv, lugar_m)
                st.success(f"✅ Ciclo reiniciado.")
                st.balloons()
                time.sleep(2)
                st.rerun()

elif selected == "Historial":
    st.subheader("🕒 Expediente Individual")
    df_v = ejecutar_query(fetch=True)
    if not df_v.empty:
        u_busq = st.selectbox("🔍 Seleccionar Vehículo:", df_v['codigo_tcs'])
        
        # --- DATOS DE LA UNIDAD ---
        unidad_info = df_v[df_v['codigo_tcs'] == u_busq].iloc[0]
        
        km_inicio = int(unidad_info['km_ultimo_manto'])
        km_actual = int(unidad_info['km_actual'])
        frecuencia = int(unidad_info['frecuencia'])
        
        # --- CÁLCULOS PRECISOS ---
        proximo_manto = km_inicio + frecuencia
        faltante = proximo_manto - km_actual
        
        # --- DISEÑO DE MÉTRICAS 
        col1, col2, col3 = st.columns(3)
        
        # 1. INICIO
        col1.metric("KM INICIO", f"{km_inicio:,} KM")
        
        # 2. ACTUAL
        col2.metric("KM ACTUAL", f"{km_actual:,} KM")
        
        # 3. PRÓXIMO MANTENIMIENTO
        # Usamos delta para mostrar cuánto falta o cuánto se pasó
        label_delta = "restantes" if faltante >= 0 else "excedidos"
        col3.metric(
            "PRÓXIMO MANTO.", 
            f"{proximo_manto:,} KM", 
            f"{faltante:,} KM {label_delta}", 
            delta_color="normal" if faltante >= 0 else "inverse"
        )
        
        st.markdown("---")

        # --- TABLA DE HISTORIAL ---
        hist = ejecutar_query(fetch=True, tabla="historial")
        if not hist.empty:
            hist_filtrado = hist[hist['codigo_tcs'] == u_busq].copy()
            
            
            hist_filtrado = hist_filtrado.sort_index(ascending=False)
            
            st.dataframe(
                hist_filtrado[['fecha', 'accion', 'kilometraje', 'lugar']], 
                use_container_width=True, 
                hide_index=True
            )
        else:
            st.info("No hay registros de movimientos para esta unidad.")
elif selected == "Nueva Unidad":
    st.subheader("🚚 Alta de Vehículo")
    with st.form("new_unit_form"):
        c1, c2 = st.columns(2)
        cod = c1.text_input("Código TCS")
        pla = c1.text_input("Placa")
        mar = c2.text_input("Marca / Modelo")
        fre = c2.selectbox("Frecuencia (KM)", [5000, 7500, 10000, 15000])
        ini = c1.number_input("Kilometraje Inicial", min_value=0, step=1)
        if st.form_submit_button("REGISTRAR UNIDAD"):
            if cod and pla:
                ejecutar_query("INSERT INTO vehiculos", (cod, pla, mar, fre, ini, ini))
                registrar_historial(cod, "ALTA", ini, "Base Central")
                st.success("✅ Unidad agregada.")
                st.rerun()

elif selected == "Ajustes":
    st.subheader("⚙️ Configuración")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### Exportar Reporte Ejecutivo")
        if st.button("📊 GENERAR EXCEL CORPORATIVO"):
            df_raw = ejecutar_query("SELECT codigo_tcs, placa, marca, km_ultimo_manto, km_actual, frecuencia FROM vehiculos", fetch=True)
            if not df_raw.empty:
                df_raw['Prox. Manto'] = df_raw['km_ultimo_manto'] + df_raw['frecuencia']
                df_raw['KM Faltantes'] = df_raw['Prox. Manto'] - df_raw['km_actual']
                df_raw['Estado'] = df_raw['KM Faltantes'].apply(lambda x: 'CRÍTICO' if x < 200 else ('ALERTA' if x < 600 else 'OPERATIVO'))
                df_raw.columns = ['CÓDIGO', 'PLACA', 'MARCA', 'U. MANTO (KM)', 'KM ACTUAL', 'FRECUENCIA', 'PRÓX. MANTO', 'FALTAN (KM)', 'ESTADO']

                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    df_raw.to_excel(writer, index=False, sheet_name='Reporte', startrow=5)
                    workbook  = writer.book
                    worksheet = writer.sheets['Reporte']

                    # --- CONFIGURACIÓN PARA IMPRESIÓN EN UNA HOJA HORIZONTAL ---

                    worksheet.set_landscape()      # Orientación Horizontal
                    worksheet.set_paper(9)         # Tamaño A4
                    worksheet.fit_to_pages(1, 1)   # Ajustar a 1 página de ancho y 1 de alto
                    worksheet.set_margins(0.3, 0.3, 0.3, 0.3) # Márgenes estrechos para ganar espacio
                    worksheet.hide_gridlines(2)

                    # FORMATOS
                    header_fmt = workbook.add_format({'bold': True, 'bg_color': '#1f6feb', 'font_color': 'white', 'border': 1, 'align': 'center', 'valign': 'vcenter'})
                    logo_fmt = workbook.add_format({'align': 'center', 'valign': 'vcenter','border': 0})
                    cell_center = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'border': 1})
                    title_fmt = workbook.add_format({'bold': True, 'font_size': 14, 'font_color': '#1f6feb', 'align': 'center', 'valign': 'vcenter'})
                    info_fmt = workbook.add_format({'font_size': 9, 'italic': True, 'align': 'center'})
                    firma_fmt = workbook.add_format({'align': 'center', 'bold': True, 'font_size': 10})
                    cargo_fmt = workbook.add_format({'align': 'center', 'bold': True, 'font_size': 9, 'top': 1})

                    # LOGO Y ENCABEZADO

                    worksheet.merge_range('A1:B4', "", logo_fmt)
                    if os.path.exists("logo.png"):
                        worksheet.insert_image('A1', 'logo.png', {'x_scale': 0.10, 'y_scale': 0.10, 'x_offset': 35, 'y_offset': 10})

                    worksheet.merge_range('C1:I2', 'SISTEMA DE GESTIÓN DE CALIDAD', title_fmt)
                    worksheet.merge_range('C3:I3', f"Fecha de Emisión: {datetime.now().strftime('%d/%m/%Y %H:%M')}", info_fmt)
                    worksheet.merge_range('C4:I4', "MANTENIMIENTO PREVENTIVO UNIDADES - TECSERM S.A.C. 2026", info_fmt)

                    # TABLA
                    for col_num, value in enumerate(df_raw.columns.values):
                        worksheet.write(5, col_num, value, header_fmt)
                        worksheet.set_column(col_num, col_num, 14)

                    for row_num, row_data in enumerate(df_raw.values):
                        for col_num, cell_value in enumerate(row_data):
                            if col_num == 8:
                                color = '#3fb950' if cell_value == 'OPERATIVO' else ('#d29922' if cell_value == 'ALERTA' else '#f85149')
                                est_fmt = workbook.add_format({'bg_color': color, 'font_color': 'white', 'bold': True, 'border': 1, 'align': 'center'})
                                worksheet.write(row_num + 6, col_num, cell_value, est_fmt)
                            else:
                                worksheet.write(row_num + 6, col_num, cell_value, cell_center)

                    # FIRMAS

                    f_idx = len(df_raw) + 9
                    worksheet.merge_range(f_idx, 1, f_idx, 3, "V°B° LOGISTICA", cargo_fmt)
                    worksheet.merge_range(f_idx + 1, 1, f_idx + 1, 3, "JUAN CARLOS ZEGARRA LOPEZ", firma_fmt)
                    worksheet.merge_range(f_idx, 5, f_idx, 7, "V°B° CALIDAD", cargo_fmt)
                    worksheet.merge_range(f_idx + 1, 5, f_idx + 1, 7, "AARON FLORES VILLANUEVA", firma_fmt)
                st.download_button(label="⬇️ Descargar Reporte_Excel", data=output.getvalue(), file_name=f"Reporte_TECSERM_{datetime.now().strftime('%d%m')}.xlsx", mime="application/vnd.ms-excel")

    with c2:
        st.markdown("### Gestión de Datos")
        df_del = ejecutar_query(fetch=True)
        if not df_del.empty:
            target = st.selectbox("Eliminar Unidad:", df_del['codigo_tcs'])
            if st.button("❌ ELIMINAR", type="primary"):
                ejecutar_query("DELETE FROM vehiculos", (target,))
                st.success("Unidad eliminada.")
                st.rerun()