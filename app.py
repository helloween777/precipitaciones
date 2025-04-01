import streamlit as st
from supabase import create_client
import pandas as pd

# 1. Conexión a Supabase (verifica que secrets.toml tenga tus credenciales)
@st.cache_resource
def init_supabase():
    return create_client(st.secrets["SUPABASE"]["url"], st.secrets["SUPABASE"]["key"])

supabase = init_supabase()

# 2. Obtener datos con los nombres CORRECTOS
@st.cache_data
def get_data():
    try:
        data = supabase.table("precipitaciones").select("anio, pp, estacion").execute()
        return pd.DataFrame(data.data)
    except Exception as e:
        st.error(f"Error al cargar datos: {str(e)}")
        return pd.DataFrame()

df = get_data()

# 3. Verificación de datos
if not df.empty:
    st.title("Análisis de Precipitaciones")
    st.write("Datos cargados correctamente. Primeras filas:", df.head())
    
    # Gráfico principal
    st.line_chart(df.groupby("anio")["pp"].mean())
    
    # Selector de estación
    estacion = st.selectbox("Selecciona estación:", df["estacion"].unique())
    df_filtrado = df[df["estacion"] == estacion]
    st.line_chart(df_filtrado.groupby("anio")["pp"].mean())
else:
    st.warning("No se pudieron cargar los datos. Verifica:")
    st.write("- Nombre de la tabla: precipitaciones")
    st.write("- Columnas solicitadas: anio, pp, estacion")
    st.write("- Configuración de secrets.toml")
