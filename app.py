import streamlit as st
from supabase import create_client
import pandas as pd
import numpy as np
from copy import deepcopy

# 1. Conexión a Supabase
@st.cache_resource
def init_supabase():
    url = st.secrets.get("SUPABASE", {}).get("url")
    key = st.secrets.get("SUPABASE", {}).get("key")
    if not url or not key:
        st.error("Error: No se encontraron las credenciales de Supabase.")
        return None
    return create_client(url, key)

supabase = init_supabase()
if not supabase:
    st.stop()

# 2. Obtener datos de Supabase
@st.cache_data
def get_data():
    try:
        response = supabase.table("precipitaciones").select("anio, pp, estacion").execute()
        if response.data:
            df = pd.DataFrame(deepcopy(response.data))
            df["anio"] = pd.to_numeric(df["anio"], errors="coerce")  # Asegurar que 'anio' es numérico
            df["pp"] = pd.to_numeric(df["pp"], errors="coerce")      # Asegurar que 'pp' es numérico
            df.dropna(inplace=True)  # Eliminar filas con valores nulos
            return df
        else:
            st.warning("No se encontraron datos en la tabla 'precipitaciones'.")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Error al cargar datos: {e}")
        return pd.DataFrame()

df = get_data()

# 3. Interfaz en Streamlit
st.title("Análisis de Precipitaciones en Estaciones Meteorológicas")

if not df.empty:
    # Mostrar información de la base de datos
    st.success(f"Datos cargados correctamente ({len(df)} registros)")
    st.write("🔍 **Vista previa de los datos:**")
    st.dataframe(df.head(5))

    # Gráfico de precipitaciones promedio por año
    st.subheader("Precipitación Promedio por Año")
    if "pp" in df.columns and not df["pp"].isnull().all():
        st.line_chart(df.groupby("anio")["pp"].mean())
    else:
        st.warning("⚠ No hay datos válidos para graficar.")

    # Filtro interactivo por estación meteorológica
    st.subheader("Filtrar por Estación")
    estaciones_unicas = df["estacion"].dropna().unique()
    if len(estaciones_unicas) > 0:
        estacion_seleccionada = st.selectbox("Selecciona una estación:", sorted(estaciones_unicas))
        datos_filtrados = df[df["estacion"] == estacion_seleccionada]

        # Mostrar gráfico de la estación seleccionada
        st.subheader(f"Precipitación en {estacion_seleccionada}")
        if not datos_filtrados.empty:
            st.line_chart(datos_filtrados.groupby("anio")["pp"].mean())
            st.write(f"**Estadísticas para {estacion_seleccionada}**")
            st.write(datos_filtrados["pp"].describe())
        else:
            st.warning("⚠ No hay datos para esta estación.")
    else:
        st.warning("⚠ No se encontraron estaciones.")

else:
    st.warning("""
    No se encontraron datos. Verifica que:
    - La tabla en Supabase se llama exactamente **"precipitaciones"**.
    - Las columnas se llaman **"anio", "pp" y "estacion"**.
    - Las credenciales en `secrets.toml` están configuradas correctamente.
    """)

