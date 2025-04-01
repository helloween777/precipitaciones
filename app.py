import streamlit as st
from supabase import create_client
import pandas as pd

# Conexión a Supabase
@st.cache_resource
def init_supabase():
    return create_client(st.secrets["SUPABASE"]["url"], st.secrets["SUPABASE"]["key"])

supabase = init_supabase()

# Obtener datos
@st.cache_data
def get_data():
    data = supabase.table("precipitaciones").select("*").execute()
    return pd.DataFrame(data.data)

df = get_data()

# --- DIAGNÓSTICO ---
st.write("🔍 Columnas disponibles:", df.columns.tolist())
st.write("📝 Primeras filas de datos:", df.head())
