import streamlit as st
from supabase import create_client
import pandas as pd

# 1. Conexión a Supabase
@st.cache_resource
def init_supabase():
    return create_client(st.secrets["SUPABASE"]["url"], st.secrets["SUPABASE"]["key"])

supabase = init_supabase()

# 2. Obtener datos
@st.cache_data
def get_data():
    data = supabase.table("Precipitaciones_Piura").select("anio, pp, estacion").execute()
    return pd.DataFrame(data.data)

df = get_data()

# 3. Mostrar datos
st.title("Análisis de Precipitaciones")

# Verificación rápida
st.write("Primeras filas de datos:", df.head())

# 4. Gráfico por año (usando anio como año)
st.line_chart(df.groupby("anio")["pp"].mean())

# 5. Selector de estación
estacion = st.selectbox("Selecciona estación:", df["estacion"].unique())
df_filtrado = df[df["estacion"] == estacion]
st.line_chart(df_filtrado.groupby("anio")["pp"].mean())
