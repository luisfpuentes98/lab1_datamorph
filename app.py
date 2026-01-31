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

# Layout de dos columnas
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Entrada de JSON")
    json_input = st.text_area(
        "Pega tu lista de objetos JSON aquí:",
        value=json.dumps(example_data, indent=4),
        height=400
    )

with col2:
    st.subheader("2. Tabla Normalizada (Pandas)")
    if json_input:
        try:
            # Intentamos cargar el JSON
            data = json.loads(json_input)
            df = pd.json_normalize(data)
            
            # Mostramos la tabla (usamos width='stretch' por la actualización de Streamlit)
            st.dataframe(df, use_container_width=True)
            
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
                )

        except json.JSONDecodeError:
            st.error("❌ Error: El formato JSON es inválido. Revisa que cada campo y objeto esté separado por una coma.")
        except Exception as e:
            st.error(f"⚠️ Error inesperado: {e}")

# Expansor informativo al final
with st.expander("📚 Diferencia entre Esquemas"):
    st.markdown("""
    * **Esquema Fijo (SQL):** Como una 'cárcel'. Debes definir cada columna antes de insertar datos.
    * **Esquema Flexible (NoSQL):** Dinámico. Si un registro tiene campos nuevos, se guardan sin afectar al resto.
    """)
