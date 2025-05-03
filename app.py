import streamlit as st
from supabase import create_client
import pandas as pd
import matplotlib.pyplot as plt

# Conexión a Supabase
@st.cache_resource
def init_supabase():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase = init_supabase()

# Cargar datos desde Supabase
@st.cache_data
def cargar_predicciones():
    try:
        data = supabase.table("predicciones_inundaciones").select("id_punto, fecha, riesgo_inundacion").execute()
        return pd.DataFrame(data.data)
    except Exception as e:
        st.error(f"Error cargando predicciones: {e}")
        return pd.DataFrame()

@st.cache_data
def cargar_puntos_inundacion():
    try:
        data = supabase.table("puntos_inundacion").select("id_punto, latitud, longitud, descripcion").execute()
        return pd.DataFrame(data.data)
    except Exception as e:
        st.error(f"Error cargando puntos de inundación: {e}")
        return pd.DataFrame()
puntos_df = cargar_puntos_inundacion()

# Cargar y mostrar los datos
df = cargar_predicciones()

st.title("Predicciones de Inundaciones")

if not df.empty:
    st.write("### Predicciones registradas")
    st.dataframe(df)

    # Convertir fecha a datetime si es necesario
    df["fecha"] = pd.to_datetime(df["fecha"])

    # Estadísticas generales
    st.subheader("Resumen estadístico de los datos")
    st.write(df.describe())

    # Estadísticas de Riesgo
    st.subheader("Estadísticas clave")
    riesgo_promedio = df["riesgo_inundacion"].mean()
    riesgo_maximo = df["riesgo_inundacion"].max()
    riesgo_minimo = df["riesgo_inundacion"].min()

    col1, col2, col3 = st.columns(3)
    col1.metric("Riesgo Promedio", f"{riesgo_promedio:.2f}")
    col2.metric("Máximo Riesgo", f"{riesgo_maximo:.2f}")
    col3.metric("Mínimo Riesgo", f"{riesgo_minimo:.2f}")

    # Riesgo promedio por fecha
    st.subheader("Riesgo promedio por fecha")
    riesgo_por_fecha = df.groupby("fecha")["riesgo_inundacion"].mean().reset_index()
    st.line_chart(riesgo_por_fecha, x="fecha", y="riesgo_inundacion")

    # Histograma de riesgos
    st.subheader("Distribución del riesgo de inundación")
    fig, ax = plt.subplots()
    df["riesgo_inundacion"].hist(bins=10, ax=ax, color='skyblue', edgecolor='black')
    ax.set_xlabel("Nivel de Riesgo")
    ax.set_ylabel("Frecuencia")
    st.pyplot(fig)

else:
    st.warning("No hay predicciones registradas.")


