import streamlit as st
from supabase import create_client
import pandas as pd

# 1. Conexión a Supabase
@st.cache_resource
def init_supabase():
    return create_client(st.secrets["SUPABASE"]["url"], st.secrets["SUPABASE"]["key"])

supabase = init_supabase()

# 2. Obtener datos con los nombres CORRECTOS de columnas
@st.cache_data
def get_data():
    try:
        data = supabase.table("precipitaciones").select("anio, pp, estacion").execute()
        return pd.DataFrame(data.data)
    except Exception as e:
        st.error(f"Error al cargar datos: {e}")
        return pd.DataFrame()

df = get_data()

# 3. Interfaz mejorada
st.title("Análisis de Precipitaciones")

if not df.empty:
    # Mostrar metadatos
    st.success(f"Datos cargados correctamente ({len(df)} registros)")
    st.write("Muestra de datos:", df.head(3))
    
    # Gráfico principal
    st.write("Precipitación promedio por año")
    st.line_chart(df.groupby("anio")["pp"].mean())
    
    # Filtro interactivo
    st.write("Filtrar por estación meteorológica")
    estacion = st.selectbox("Selecciona una estación:", 
                          options=sorted(df["estacion"].unique()),
                          index=0)
    
    datos_filtrados = df[df["estacion"] == estacion]
    st.line_chart(datos_filtrados.groupby("anio")["pp"].mean())
    
    # Estadísticas
    st.write(f"**Estadísticas para {estacion}**")
    st.write(datos_filtrados["pp"].describe())
else:
    st.warning("""
    No se encontraron datos. Verifica:
    1. La tabla existe y se llama exactamente "precipitaciones"
    2. Las columnas se llaman "anio", "pp" y "estacion"
    3. La configuración en secrets.toml es correcta
    """)
