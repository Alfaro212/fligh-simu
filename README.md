
# 🚀 Flight Simulator / Simulador de Vuelo Suborbital

Este es un simulador visual e interactivo de vuelo suborbital desarrollado con [Streamlit](https://streamlit.io). Permite experimentar con variables como altitud, velocidad, gravedad y combustible en tiempo real.

La aplicación tiene un **selector de idioma** que permite usarla tanto en **Español como en Inglés**.

## 🌐 Versión en línea

Puedes probar la aplicación aquí:  
👉 [https://flight-sim.streamlit.app](https://flight-sim.streamlit.ap

## 🧰 Tecnologías utilizadas

- **Python**
- **Streamlit**
- **pandas**
- **matplotlib**
- **plotly**

---

## ⚙️ Cómo ejecutar localmente

Para ejecutar la app en tu máquina local, sigue estos pasos:

1. Clona el repositorio:

   ```bash
   git clone https://github.com/tu-usuario/flight-sim.git
   cd flight-sim
   ```

2. Crea un entorno virtual (opcional, pero recomendado):

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # En Linux/Mac
   .\venv\Scripts\activate  # En Windows
   ```

3. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

4. Ejecuta la aplicación:

   ```bash
   streamlit run app.py
   ```

---

## ☁️ Despliegue en Streamlit Cloud

1. Asegúrate de que tu archivo principal se llame `app.py`.
2. En [Streamlit Cloud](https://streamlit.io/cloud), haz clic en **“+ New app”**.
3. Configura el despliegue:
   - **Repository**: `tu-usuario/flight-sim`
   - **Branch**: `main`
   - **Main file path**: `app.py`
4. Haz clic en **Deploy**.

---

## 🗣️ Selector de idioma

La app detecta el idioma seleccionado por el usuario (Español o Inglés) y actualiza los textos dinámicamente en la interfaz:

```python
idioma = st.selectbox("🌐 Idioma / Language", ["Español", "English"])
```


