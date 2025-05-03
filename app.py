import streamlit as st
from supabase import create_client
import pandas as pd

# Conexión a Supabase
@st.cache_resource
def init_supabase():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase = init_supabase()

# Obtener predicciones
@st.cache_data
def cargar_predicciones():
    try:
        data = supabase.table("predicciones_inundaciones").select("id_punto, fecha, riesgo_inundacion").execute()
        return pd.DataFrame(data.data)
    except Exception as e:
        st.error(f"Error cargando predicciones: {e}")
        return pd.DataFrame()

df = cargar_predicciones()

# Interfaz
st.title("Predicciones de Inundaciones")

if not df.empty:
    st.write("Predicciones registradas:")
    st.dataframe(df)

    # Agrupar y graficar por fecha
    st.write("Riesgo promedio de inundación por fecha:")
    st.line_chart(df.groupby("fecha")["riesgo_inundacion"].mean())

else:
    st.warning("No hay predicciones registradas.")

