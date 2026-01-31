import streamlit as st
import pandas as pd
import json

# Configuración de página
st.set_page_config(page_title="DataMorph JSON", layout="wide")
st.title("🧪 DataMorph JSON")

# JSON de ejemplo inicial
example_data = [
    {"id": 1, "nombre": "Luis Fernando", "ciudad": "Madrid"},
    {"id": 2, "nombre": "Ana Maria", "habilidades": ["AWS", "S3"]},
    {"id": 3, "nombre": "Carlos", "detalles": {"rol": "Data Engineer"}}
]

# Layout de dos columnas [cite: 17, 62]
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Entrada de JSON")
    json_input = st.text_area(
        "Pega tu lista de objetos JSON aquí:",
        value=json.dumps(example_data, indent=4),
        height=400
    ) [cite: 17, 63]

with col2:
    st.subheader("2. Tabla Normalizada (Pandas)")
    if json_input:
        try:
            data = json.loads(json_input)
            # Conversión de JSON a tabla plana [cite: 17, 64]
            df = pd.json_normalize(data)
            
            # Ajuste de ancho según la versión 2026 de Streamlit
            st.dataframe(df, width="stretch")
            
            # Analítica de Esquema [cite: 19, 66]
            st.markdown("---")
            st.subheader("📊 Analítica de Esquema")
            
            cols = df.columns.tolist()
            null_count = df.isnull().sum().sum()
            
            st.write(f"**Columnas detectadas:** {', '.join(cols)}")
            st.metric("Total de valores nulos (NaN)", null_count)
            
            if null_count > 0:
                st.warning(
                    "⚠️ **Nota de Ingeniería:** Detectamos datos dispersos (Sparse Data). "
                    "En SQL esto sería ineficiente, pero en NoSQL es normal."
                ) [cite: 19, 66]

        except json.JSONDecodeError:
            st.error("❌ Error: Formato JSON inválido.") [cite: 21, 68]
        except Exception as e:
            st.error(f"⚠️ Error: {e}")

# Explicación teórica final [cite: 21, 68]
with st.expander("📚 Diferencia entre Esquemas"):
    st.markdown("""
    * **Esquema Fijo (SQL):** Rígido. No puedes guardar datos si no definiste la columna antes[cite: 4, 51].
    * **Esquema Flexible (NoSQL):** Dinámico. Los campos nuevos se guardan sin afectar al resto[cite: 5, 52].
    """)
