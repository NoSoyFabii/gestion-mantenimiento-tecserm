import streamlit as st
import pandas as pd
import os
import time
from datetime import datetime
from streamlit_option_menu import option_menu
import io
from supabase import create_client, Client
from login_modulo import check_login
from io import BytesIO
import pytz

def cerrar_sesion():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.session_state["autenticado"] = False

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

# --- NUEVO: FUNCIÓN PARA MANTENER VIVO SUPABASE (Despertador) ---
def despertar_supabase():
    if supabase:
        try:
            # Micro-consulta para evitar la pausa por inactividad
            supabase.table("vehiculos").select("count", count="exact").limit(1).execute()
        except Exception:
            pass

# --- ACTIVACIÓN DEL DESPERTADOR (Antes del login) ---
despertar_supabase()

# --- LOGIN ---
check_login()

def ejecutar_query(query_str=None, params=(), fetch=False, tabla="vehiculos"):
    try:
        if fetch:
            res = supabase.table(tabla).select("*").execute()
            df_res = pd.DataFrame(res.data)
            
            # --- LIMPIEZA ANTIFALLO (Soluciona el error NaN to Integer) ---
            if not df_res.empty:
                if tabla == "vehiculos":
                    # Forzamos que estas columnas sean números y rellenamos vacíos con 0
                    for col in ['km_actual', 'km_ultimo_manto', 'frecuencia']:
                        if col in df_res.columns:
                            df_res[col] = pd.to_numeric(df_res[col], errors='coerce').fillna(0).astype(int)
                
                # Ordenamiento seguro
                if 'codigo_tcs' in df_res.columns:
                    df_res['codigo_tcs'] = df_res['codigo_tcs'].astype(str)
                    df_res = df_res.sort_values(by='codigo_tcs', key=lambda col: col.str.extract('(\d+)')[0].fillna(0).astype(int))
            return df_res
        
        # --- LÓGICA DE ESCRITURA ---
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
            # CORRECCIÓN: WHERE para eliminar unidad específica
            supabase.table("vehiculos").delete().eq("codigo_tcs", params[0]).execute()
        
        st.cache_data.clear()
        return True
    except Exception as e:
        st.error(f"Error en base de datos: {e}")
        return pd.DataFrame() if fetch else False

def registrar_historial(codigo, accion, km, lugar="N/A", obs=""):
    try:
        # Usamos la hora de Perú para el registro
        peru_tz = pytz.timezone('America/Lima')
        fecha_hoy = datetime.now(peru_tz).strftime("%d/%m/%Y %H:%M")
        
        data = {
            "fecha": fecha_hoy, 
            "codigo_tcs": str(codigo), 
            "accion": accion, 
            "kilometraje": int(km), 
            "lugar": lugar,
            "observaciones": obs  # <--- Esta es la clave para el Excel
        }
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
        options=["Panel Control", "Registrar KM", "Nueva Unidad", "Mantenimiento Preventivo", "Mantenimiento Correctivo", "Historial", "Ajustes"],
        icons=["grid-fill", "speedometer", "plus-circle", "tools", "wrench", "clock-history", "gear"],
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

elif selected == "Mantenimiento Preventivo":
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
    
    tz_peru = pytz.timezone('America/Lima')
    
    df_v = ejecutar_query(fetch=True)
    if not df_v.empty:
        u_busq = st.selectbox("🔍 Seleccionar Vehículo:", df_v['codigo_tcs'])
        
        unidad_info = df_v[df_v['codigo_tcs'] == u_busq].iloc[0]
        placa_v = unidad_info['placa']
        marca_v = unidad_info['marca']
        
        st.markdown("---")

        hist = ejecutar_query(fetch=True, tabla="historial")
        if not hist.empty:
            # 1. Procesar datos: Filtrar y calcular KM Anterior
            hist_filtrado = hist[hist['codigo_tcs'] == u_busq].copy()
            hist_filtrado['kilometraje'] = pd.to_numeric(hist_filtrado['kilometraje'], errors='coerce').fillna(0).astype(int)
            
            # Aseguramos que la columna observaciones exista en el dataframe
            if 'observaciones' not in hist_filtrado.columns:
                hist_filtrado['observaciones'] = ""
            else:
                hist_filtrado['observaciones'] = hist_filtrado['observaciones'].fillna("")

            # Ordenamos por fecha para que el cálculo del anterior sea real
            hist_filtrado = hist_filtrado.sort_values(by='fecha', ascending=True)
            hist_filtrado['KM_ANTERIOR'] = hist_filtrado['kilometraje'].shift(1).fillna(0).astype(int)
            
            # Reordenar para mostrar lo más reciente arriba
            df_final = hist_filtrado.sort_index(ascending=False)

            # --- GENERACIÓN DE EXCEL ---
            output_h = io.BytesIO()
            with pd.ExcelWriter(output_h, engine='xlsxwriter') as writer:
                # AÑADIDO: 'observaciones' a la exportación
                df_export = df_final[['fecha', 'accion', 'KM_ANTERIOR', 'kilometraje', 'lugar', 'observaciones']].copy()
                df_export.columns = ['FECHA/HORA', 'ACTIVIDAD', 'KM ANTERIOR', 'KM ACTUAL', 'UBICACIÓN/TALLER', 'OBSERVACIONES']
                
                # Escribimos los datos (fila 7)
                df_export.to_excel(writer, index=False, sheet_name='CONTROL_TCS', startrow=6, header=False)
                
                workbook  = writer.book
                worksheet = writer.sheets['CONTROL_TCS']

                # --- CONFIGURACIÓN DE PÁGINA ---
                worksheet.set_landscape() 
                worksheet.set_paper(9)    # A4
                worksheet.fit_to_pages(1, 0) 

                # --- FORMATOS ---
                header_fmt = workbook.add_format({'bold': True, 'bg_color': '#1f6feb', 'font_color': 'white', 'border': 1, 'align': 'center', 'valign': 'vcenter'})
                # Formato especial con text_wrap para que las observaciones no se corten
                data_fmt = workbook.add_format({'border': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True})
                title_fmt = workbook.add_format({'bold': True, 'font_size': 16, 'font_color': '#1f6feb', 'align': 'center'})
                info_fmt = workbook.add_format({'align': 'center', 'bold': True})
                firma_fmt = workbook.add_format({'align': 'center', 'bold': True, 'top': 2})

                # --- ENCABEZADO Y LOGO ---
                if os.path.exists("logo.png"):
                    worksheet.insert_image('A1', 'logo.png', {'x_scale': 0.16, 'y_scale': 0.16})
                
                # Expandimos el rango de mezcla de celdas hasta la columna F
                worksheet.merge_range('C1:F2', 'REPORTE DE CONTROL VEHICULAR', title_fmt)
                worksheet.merge_range('C3:F3', f"UNIDAD: {u_busq}  |  PLACA: {placa_v}", info_fmt)
                worksheet.merge_range('C4:F4', f"MARCA: {marca_v}", workbook.add_format({'align': 'center'}))
                
                fecha_peru = datetime.now(tz_peru).strftime('%d/%m/%Y %H:%M')
                worksheet.merge_range('C5:F5', f"FECHA IMPRESIÓN: {fecha_peru}", workbook.add_format({'align': 'center', 'italic': True, 'font_size': 10}))

                # --- ANCHO DE COLUMNAS ACTUALIZADO ---
                worksheet.set_column('A:A', 18) # Fecha
                worksheet.set_column('B:B', 25) # Actividad
                worksheet.set_column('C:D', 14) # KM Anterior y Actual
                worksheet.set_column('E:E', 25) # Ubicación
                worksheet.set_column('F:F', 40) # OBSERVACIONES (Más ancha)

                # --- ESCRIBIR CABECERAS ---
                for col_num, value in enumerate(df_export.columns.values):
                    worksheet.write(6, col_num, value, header_fmt)

                # --- ESCRIBIR DATOS ---
                for row_num, row_data in enumerate(df_export.values):
                    for col_num, cell_value in enumerate(row_data):
                        worksheet.write(row_num + 7, col_num, cell_value, data_fmt)

                # --- FIRMAS ---
                f_row = len(df_export) + 10
                worksheet.merge_range(f_row, 0, f_row, 1, "V°B° LOGISTICA", firma_fmt)
                # Movido a la derecha para equilibrar con la nueva columna
                worksheet.merge_range(f_row, 4, f_row, 5, "V°B° CALIDAD", firma_fmt)

            # Botón de descarga
            st.download_button(
                label="📥 DESCARGAR REPORTE DE AUDITORÍA COMPLETO",
                data=output_h.getvalue(),
                file_name=f"AUDITORIA_{u_busq}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

            # Vista en tabla (Añadida la columna observaciones también aquí)
            st.dataframe(df_final[['fecha', 'accion', 'KM_ANTERIOR', 'kilometraje', 'lugar', 'observaciones']], use_container_width=True, hide_index=True)
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

elif selected == "Mantenimiento Correctivo":
    st.subheader("🛠️ Registro de Mantenimiento Correctivo (Eventual)")
    st.info("Registre aquí reparaciones, cambios de llantas o cualquier actividad fuera del mantenimiento preventivo.")
    
    df_v = ejecutar_query(fetch=True)
    if not df_v.empty:
        u_sel = st.selectbox("Seleccione la Unidad afectada:", df_v['codigo_tcs'])
        
        # --- FORMULARIO DE REGISTRO ---
        with st.form("form_manto_correctivo"):
            col1, col2 = st.columns(2)
            f_inicio = col1.date_input("Fecha de Ingreso", value=datetime.now(), format="DD/MM/YYYY")
            f_fin = col2.date_input("Fecha de Salida", value=datetime.now(), format="DD/MM/YYYY")   
            
            actividad = st.text_input("Actividad realizada", placeholder="Ej: Cambio de neumáticos delanteros")
            costo_mant = st.number_input("Costo del servicio (S/.)", min_value=0.0, step=0.50)
            
            # Estas son las observaciones que el auditor quiere ver detalladas
            comentarios = st.text_area("Observaciones / Detalles técnicos")
            
            if st.form_submit_button("💾 REGISTRAR"):
                if actividad:
                    data_corr = {
                        "fecha_inicio": str(f_inicio),
                        "fecha_fin": str(f_fin),
                        "codigo_tcs": u_sel,
                        "descripcion": actividad,
                        "observaciones": comentarios, # NUEVO: Guardado en tabla correctiva
                        "costo": float(costo_mant)
                    }
                    
                    try:
                        # 1. Guardar en tabla específica de correctivos
                        supabase.table("mantenimiento_correctivo").insert(data_corr).execute()
                        
                        # 2. NUEVO: Guardar en Historial General pasando los comentarios
                        # Ahora incluimos 'comentarios' al final para que aparezcan en el Excel
                        registrar_historial(u_sel, f"CORRECTIVO: {actividad}", 0, "Taller Externo", comentarios)
                        
                        st.success(f"✅ Registro guardado con éxito para la unidad {u_sel}")
                        st.balloons()
                        time.sleep(1.5)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error al guardar: {e}")
                else:
                    st.warning("⚠️ La descripción de la actividad es obligatoria.")

        # --- TABLA DE VISUALIZACIÓN RÁPIDA ---
        st.markdown("---")
        st.subheader(f"📋 Últimos correctivos de la unidad {u_sel}")
        
        try:
            res_c = supabase.table("mantenimiento_correctivo").select("*").eq("codigo_tcs", u_sel).order("fecha_inicio", desc=True).limit(5).execute()
            df_corr = pd.DataFrame(res_c.data)
            
            if not df_corr.empty:
                df_view = df_corr[['fecha_inicio', 'fecha_fin', 'descripcion', 'costo', 'observaciones']].copy()
                df_view.columns = ['F. INICIO', 'F. FIN', 'ACTIVIDAD', 'COSTO (S/.)', 'OBSERVACIONES']
                st.dataframe(df_view, use_container_width=True, hide_index=True)
            else:
                st.write("No hay mantenimientos correctivos registrados para esta unidad.")
        except Exception as e:
            st.error(f"No se pudo cargar la tabla de visualización: {e}")

elif selected == "Ajustes":
    st.subheader("⚙️ Configuración")
    
    # --- CONFIGURACIÓN DE HORA PERÚ ---
    peru_tz = pytz.timezone('America/Lima')
    fecha_peru = datetime.now(peru_tz)
    
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("### Exportar Reporte Ejecutivo")
        if st.button("📊 GENERAR EXCEL CORPORATIVO"):
            df_raw = ejecutar_query("SELECT codigo_tcs, placa, marca, km_ultimo_manto, km_actual, frecuencia FROM vehiculos", fetch=True)
            
            if not df_raw.empty:
                # Cálculos lógicos
                df_raw['Prox. Manto'] = df_raw['km_ultimo_manto'] + df_raw['frecuencia']
                df_raw['KM Faltantes'] = df_raw['Prox. Manto'] - df_raw['km_actual']
                df_raw['Estado'] = df_raw['KM Faltantes'].apply(lambda x: 'CRÍTICO' if x < 200 else ('ALERTA' if x < 600 else 'OPERATIVO'))
                
                # Renombrar columnas para el Excel
                df_raw.columns = ['CÓDIGO', 'PLACA', 'MARCA', 'FRECUENCIA', 'U. MANTO (KM)', 'KM ACTUAL', 'PRÓX. MANTO', 'FALTAN (KM)', 'ESTADO']

                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    df_raw.to_excel(writer, index=False, sheet_name='Reporte', startrow=5)
                    workbook  = writer.book
                    worksheet = writer.sheets['Reporte']

                    # --- CONFIGURACIÓN PARA IMPRESIÓN ---
                    worksheet.set_landscape()
                    worksheet.set_paper(9) # A4
                    worksheet.fit_to_pages(1, 1)
                    worksheet.set_margins(0.3, 0.3, 0.3, 0.3)
                    worksheet.hide_gridlines(2)

                    # FORMATOS
                    header_fmt = workbook.add_format({'bold': True, 'bg_color': '#1f6feb', 'font_color': 'white', 'border': 1, 'align': 'center', 'valign': 'vcenter'})
                    logo_fmt = workbook.add_format({'align': 'center', 'valign': 'vcenter','border': 0})
                    cell_center = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'border': 1})
                    title_fmt = workbook.add_format({'bold': True, 'font_size': 14, 'font_color': '#1f6feb', 'align': 'center', 'valign': 'vcenter'})
                    info_fmt = workbook.add_format({'font_size': 9, 'italic': True, 'align': 'center'})
                    firma_fmt = workbook.add_format({'align': 'center', 'bold': True, 'font_size': 10})
                    cargo_fmt = workbook.add_format({'align': 'center', 'bold': True, 'font_size': 9, 'top': 1})

                    # LOGO Y ENCABEZADO (CON HORA DE PERÚ)
                    worksheet.merge_range('A1:B4', "", logo_fmt)
                    if os.path.exists("logo.png"):
                        worksheet.insert_image('A1', 'logo.png', {'x_scale': 0.10, 'y_scale': 0.10, 'x_offset': 35, 'y_offset': 10})

                    worksheet.merge_range('C1:I2', 'SISTEMA DE GESTIÓN DE CALIDAD', title_fmt)
                    # Aquí se aplica la fecha corregida
                    worksheet.merge_range('C3:I3', f"Fecha de Emisión: {fecha_peru.strftime('%d/%m/%Y %H:%M')}", info_fmt)
                    worksheet.merge_range('C4:I4', "MANTENIMIENTO PREVENTIVO UNIDADES - TECSERM S.A.C. 2026", info_fmt)

                    # ESCRIBIR TABLA
                    for col_num, value in enumerate(df_raw.columns.values):
                        worksheet.write(5, col_num, value, header_fmt)
                        worksheet.set_column(col_num, col_num, 14)

                    for row_num, row_data in enumerate(df_raw.values):
                        for col_num, cell_value in enumerate(row_data):
                            if col_num == 8: # Columna ESTADO
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
                
                # Botón de descarga con nombre de archivo dinámico (Hora Perú)
                st.download_button(
                    label="⬇️ Descargar Reporte_Excel", 
                    data=output.getvalue(), 
                    file_name=f"Reporte_TECSERM_{fecha_peru.strftime('%d%m_%H%M')}.xlsx", 
                    mime="application/vnd.ms-excel"
                )

    with c2:
        st.markdown("### Gestión de Datos")
        # Obtenemos la lista actualizada para el selector
        df_del = ejecutar_query("SELECT codigo_tcs FROM vehiculos", fetch=True)
        if not df_del.empty:
            target = st.selectbox("Seleccionar Unidad para Eliminar:", df_del['codigo_tcs'])
            # Botón de eliminar con confirmación visual de Streamlit
            if st.button("❌ ELIMINAR UNIDAD", type="primary"):
                # CORRECCIÓN: Se añade WHERE para no borrar toda la tabla
                ejecutar_query("DELETE FROM vehiculos WHERE codigo_tcs = %s", (target,))
                st.success(f"Unidad {target} eliminada correctamente.")
                st.rerun()
        else:
            st.info("No hay unidades registradas para eliminar.")