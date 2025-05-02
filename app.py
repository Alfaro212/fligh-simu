
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import time

# 🌐 Selector de idioma
idioma = st.sidebar.selectbox("🌐 Idioma / Language", ["Español", "English"])

# Diccionario de traducciones
textos = {
    "title": {
        "Español": "Simulador de Vuelo Suborbital",
        "English": "Suborbital Flight Simulator"
    },
    "altura": {
        "Español": "Altura inicial (km)",
        "English": "Initial height (km)"
    },
    "velocidad": {
        "Español": "Velocidad inicial (km/s)",
        "English": "Initial speed (km/s)"
    },
    "gravedad": {
        "Español": "Gravedad (m/s²)",
        "English": "Gravity (m/s²)"
    },
    "combustible": {
        "Español": "Combustible (kg)",
        "English": "Fuel (kg)"
    },
    "simular": {
        "Español": "Iniciar simulación",
        "English": "Start Simulation"
    },
    "grafico_altura": {
        "Español": "Altura vs Tiempo",
        "English": "Altitude vs Time"
    },
    "eje_tiempo": {
        "Español": "Tiempo (s)",
        "English": "Time (s)"
    },
    "eje_altura": {
        "Español": "Altura (km)",
        "English": "Altitude (km)"
    },
}

# --- PHYSICS FUNCTIONS ---

def gravity(alt):
    R = 6371000  # Earth radius in meters
    return 9.81 * (R / (R + alt))**2

def air_density(alt):
    if alt < 10000:
        return 1.225 * (1 - alt / 10000)**4.256
    else:
        return 0

def simulate_rocket(thrust, dry_mass, fuel_mass, burn_rate, Cd, A, dt):
    mass = dry_mass + fuel_mass
    velocity = 0.0
    altitude = 0.0
    time_sec = 0.0

    data = []

    while altitude >= 0:
        g = gravity(altitude)
        rho = air_density(altitude)
        drag = 0.5 * rho * velocity**2 * Cd * A
        drag *= -1 if velocity > 0 else 1

        if fuel_mass > 0:
            actual_thrust = thrust
            fuel_used = min(burn_rate * dt, fuel_mass)
            fuel_mass -= fuel_used
            mass -= fuel_used
        else:
            actual_thrust = 0

        weight = mass * g
        net_force = actual_thrust - weight - drag
        acceleration = net_force / mass
        velocity += acceleration * dt
        altitude += velocity * dt
        time_sec += dt

        data.append({
            "Time (s)": time_sec,
            "Altitude (m)": altitude,
            "Velocity (m/s)": velocity,
            "Acceleration (m/s²)": acceleration
        })

    return pd.DataFrame(data)

# --- STREAMLIT INTERFACE ---
st.title("🚀 Suborbital Rocket Flight Simulator")

st.sidebar.header("Rocket Parameters")
thrust = st.sidebar.slider("Thrust (N)", 5000, 50000, 20000, step=1000)
dry_mass = st.sidebar.number_input("Dry mass (kg)", 100.0, 10000.0, 1000.0)
fuel_mass = st.sidebar.number_input("Fuel mass (kg)", 0.0, 10000.0, 500.0)
burn_rate = st.sidebar.number_input("Fuel consumption rate (kg/s)", 0.1, 100.0, 5.0)
Cd = st.sidebar.slider("Drag coefficient (Cd)", 0.1, 1.5, 0.5)
A = st.sidebar.number_input("Frontal area (m²)", 0.1, 10.0, 1.0)
dt = st.sidebar.number_input("Time step (s)", 0.01, 1.0, 0.1)

if st.button("🚀 Launch Simulation"):
    df_simulated = simulate_rocket(thrust, dry_mass, fuel_mass, burn_rate, Cd, A, dt)

    st.success("✅ Simulation completed")

    max_alt = df_simulated['Altitude (m)'].max()
    max_vel = df_simulated['Velocity (m/s)'].max()
    max_acc = df_simulated['Acceleration (m/s²)'].max()

    col1, col2, col3 = st.columns(3)
    col1.metric("Max Altitude", f"{max_alt:.2f} m")
    col2.metric("Max Velocity", f"{max_vel:.2f} m/s")
    col3.metric("Max Acceleration", f"{max_acc:.2f} m/s²")

    st.subheader("📈 Visualization Options")
    options = st.multiselect("Select values to display:",
                             ["Altitude (m)", "Velocity (m/s)", "Acceleration (m/s²)"],
                             default=["Altitude (m)", "Velocity (m/s)", "Acceleration (m/s²)"])

    if options:
        st.line_chart(df_simulated.set_index("Time (s)")[options])

    if st.checkbox("🎬 Animate rocket flight (2D height vs. time)"):
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=[], y=[],
            mode="lines+markers",
            line=dict(color="orange"),
            name="Rocket Trajectory"
        ))
        fig.update_layout(
            xaxis_title="Time (s)",
            yaxis_title="Altitude (m)",
            title="Rocket Ascent"
        )

        graph = st.plotly_chart(fig, use_container_width=True)
        for i in range(1, len(df_simulated), 5):
            fig.data[0].x = df_simulated["Time (s)"][:i]
            fig.data[0].y = df_simulated["Altitude (m)"][:i]
            graph.plotly_chart(fig, use_container_width=True)
            time.sleep(0.05)

    if st.checkbox("📋 Show raw data"):
        st.dataframe(df_simulated)

    st.subheader("📁 Optional: Compare with real flight data")
    file = st.file_uploader("Upload CSV with columns: Time (s), Altitude (m), Velocity (m/s)", type=["csv"])
    if file:
        df_real = pd.read_csv(file)
        st.line_chart({
            "Simulated Altitude (m)": df_simulated["Altitude (m)"].values,
            "Real Altitude (m)": df_real["Altitude (m)"].values[:len(df_simulated)]
        })
