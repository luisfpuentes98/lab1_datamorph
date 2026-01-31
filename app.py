import streamlit as st
import pandas as pd
import json

# 1. Configuración de la aplicación
st.set_page_config(page_title="DataMorph JSON", layout="wide")
st.title("🧪 DataMorph JSON")

# 2. Datos de ejemplo iniciales (Esquema Flexible)
example_data = [
    {"id": 1, "nombre": "Luis Fernando", "ciudad": "Madrid"},
    {"id": 2, "nombre": "Ana Maria", "habilidades": ["AWS", "S3"]},
    {"id": 3, "nombre": "Carlos", "detalles": {"rol": "Data Engineer"}}
]

# 3. Creación de la interfaz en dos columnas
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
            # Procesamiento de los datos
            data = json.loads(json_input)
            df = pd.json_normalize(data)
            
            # Visualización de la tabla
            st.dataframe(df, width="stretch")
            
            # 4. Analítica de Esquema (Paso B del laboratorio)
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
            st.error("❌ Error: El formato JSON es inválido. Revisa las comas y llaves.")
        except Exception as e:
            st.error(f"⚠️ Error inesperado: {e}")

# 5. Explicación teórica (Paso C del laboratorio)
st.markdown("---")
with st.expander("📚 Diferencia entre Esquemas"):
    st.markdown("""
    * **Esquema Fijo (SQL):** Como una 'cárcel'. Debes definir cada columna antes de insertar datos.
    * **Esquema Flexible (NoSQL):** Dinámico. Si un registro tiene campos nuevos, se guardan sin afectar al resto.
    """)
