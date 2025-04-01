import streamlit as st
from supabase import create_client
import pandas as pd

# Conexión a Supabase
supabase = create_client(st.secrets["SUPABASE"]["url"], st.secrets["SUPABASE"]["key"])
data = supabase.table("precipitaciones").select("*").execute()
df = pd.DataFrame(data.data)

# Ver datos y columnas
st.write("📋 **Columnas en tus datos:**", df.columns.tolist())  # 👈 Esto te mostrará los nombres REALES
st.write("📊 **Datos:**", df)  # 👈 Esto muestra tu tabla completa

# Gráfico (cambia "anio" y "pp" por los nombres REALES que veas arriba)
st.line_chart(df.groupby("anio")["pp"].mean())  # ✏️ Edita aquí!