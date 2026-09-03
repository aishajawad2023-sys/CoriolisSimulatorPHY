import streamlit as st
import numpy as np
import plotly.graph_objects as go

from physics import (
vertical_circle,
coriolis_acceleration,
coriolis_parameter,
earth_rotation_rate,
simulate_circular_motion,
)

st.set_page_config(
page_title="Coriolis — The Rotating World Simulator",
page_icon="🌍",
layout="wide",
)

st.title("🌍 Coriolis — The Rotating World Simulator")
st.caption("A computational physics simulator for circular motion, rotating frames, and the Coriolis effect.")

st.sidebar.title("Simulation Mode")

mode = st.sidebar.radio(
"Choose a mode:",
[
"Circular Motion",
"Vertical Circle",
"Coriolis Effect",
"Earth Mode",
],
)

st.sidebar.markdown("---")
st.sidebar.info(
"This simulator uses numerical physics calculations and interactive Plotly visualizations."
)

# ============================================================

# CIRCULAR MOTION

# ============================================================

if (
        run
        or "circular_simulation" not in st.session_state
        or st.session_state.get("circular_parameters") != simulation_parameters
    ):

        times, positions, velocities = simulate_circular_motion(
            radius=radius,
            omega=omega,
            total_time=simulation_time,
            dt=0.01,
        )
          

with col1:
    radius = st.slider(
        "Radius (m)",
        min_value=1.0,
        max_value=50.0,
        value=20.0,
        step=1.0,
    )

with col2:
    omega = st.slider(
        "Angular velocity ω (rad/s)",
        min_value=0.1,
        max_value=10.0,
        value=2.0,
        step=0.1,
    )

with col3:
    simulation_time = st.slider(
        "Simulation time (s)",
        min_value=1.0,
        max_value=20.0,
        value=10.0,
        step=1.0,
    )

run = st.button(
    "▶ Run simulation",
    type="primary",
    use_container_width=True,
)

simulation_parameters = (
    radius,
    omega,
    simulation_time,
)

if (
    run
    or "circular_simulation" not in st.session_state
    or st.session_state.get("circular_parameters") != simulation_parameters
):

    times, positions, velocities = simulate_circular_motion(
        radius=radius,
        omega=omega,
        total_time=simulation_time,
        dt=0.01,
    )

    st.session_state.circular_simulation = (
        times,
        positions,
        velocities,
    )

    st.session_state.circular_parameters = simulation_parameters

times, positions, velocities = st.session_state.circular_simulation

frame = st.slider(
    "Simulation time",
    min_value=0,
    max_value=len(times) - 1,
    value=0,
    step=1,
)

current_time = times[frame]
current_position = positions[frame]
current_velocity = velocities[frame]

acceleration = -omega**2 * current_position

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Time",
        f"{current_time:.2f} s",
    )

with col2:
    st.metric(
        "Speed",
        f"{np.linalg.norm(current_velocity):.2f} m/s",
    )

with col3:
    st.metric(
        "Acceleration",
        f"{np.linalg.norm(acceleration):.2f} m/s²",
    )

with col4:
    st.metric(
        "Radius",
        f"{np.linalg.norm(current_position):.2f} m",
    )

st.markdown("---")

fig = go.Figure()

# Full trajectory
fig.add_trace(
    go.Scatter(
        x=positions[:, 0],
        y=positions[:, 1],
        mode="lines",
        name="Trajectory",
        line=dict(width=3),
    )
)

# Current particle
fig.add_trace(
    go.Scatter(
        x=[current_position[0]],
        y=[current_position[1]],
        mode="markers",
        name="Particle",
        marker=dict(
            size=14,
        ),
    )
)

# Center
fig.add_trace(
    go.Scatter(
        x=[0],
        y=[0],
        mode="markers",
        name="Center",
        marker=dict(
            size=10,
        ),
    )
)

# Velocity vector
vector_scale = 2.0

fig.add_trace(
    go.Scatter(
        x=[
            current_position[0],
            current_position[0] + current_velocity[0] * vector_scale,
        ],
        y=[
            current_position[1],
            current_position[1] + current_velocity[1] * vector_scale,
        ],
        mode="lines",
        name="Velocity",
        line=dict(width=4),
    )
)

# Acceleration vector
acceleration_scale = 1.0

fig.add_trace(
    go.Scatter(
        x=[
            current_position[0],
            current_position[0] + acceleration[0] * acceleration_scale,
        ],
        y=[
            current_position[1],
            current_position[1] + acceleration[1] * acceleration_scale,
        ],
        mode="lines",
        name="Acceleration",
        line=dict(width=4),
    )
)

fig.update_layout(
    title="Circular Motion",
    xaxis_title="x position (m)",
    yaxis_title="y position (m)",
    xaxis=dict(
        scaleanchor="y",
        scaleratio=1,
    ),
    height=650,
    legend=dict(
        orientation="h",
    ),
)

st.plotly_chart(
    fig,
    use_container_width=True,
)

st.subheader("Physics")

st.latex(r"a_c = \omega^2 r")

st.latex(r"v = \omega r")

st.markdown(
    f"""
    **Current values**

    - Radius: `{radius:.2f} m`
    - Angular velocity: `{omega:.2f} rad/s`
    - Speed: `{omega * radius:.2f} m/s`
    - Centripetal acceleration: `{omega**2 * radius:.2f} m/s²`
    """
)


# ============================================================

# VERTICAL CIRCLE

# ============================================================

elif mode == "Vertical Circle":

```
st.header("🟢 Vertical Circle")

col1, col2 = st.columns(2)

with col1:
    radius = st.slider(
        "Radius (m)",
        min_value=1.0,
        max_value=30.0,
        value=10.0,
        step=1.0,
    )

with col2:
    gravity = st.slider(
        "Gravity (m/s²)",
        min_value=1.0,
        max_value=20.0,
        value=9.81,
        step=0.01,
    )

theta, x, y, velocity = vertical_circle(
    radius=radius,
    gravity=gravity,
)

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=x,
        y=y,
        mode="lines",
        name="Vertical Circle",
        line=dict(width=3),
    )
)

fig.add_trace(
    go.Scatter(
        x=[0],
        y=[0],
        mode="markers",
        name="Center",
        marker=dict(size=10),
    )
)

fig.update_layout(
    title="Vertical Circular Path",
    xaxis_title="x position (m)",
    yaxis_title="y position (m)",
    xaxis=dict(
        scaleanchor="y",
        scaleratio=1,
    ),
    height=650,
)

st.plotly_chart(
    fig,
    use_container_width=True,
)

st.subheader("Minimum Speeds")

v_top_min = np.sqrt(gravity * radius)
v_bottom_min = np.sqrt(5 * gravity * radius)

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Minimum speed at top",
        f"{v_top_min:.2f} m/s",
    )

with col2:
    st.metric(
        "Minimum speed at bottom",
        f"{v_bottom_min:.2f} m/s",
    )

st.markdown(
    """
    For an object to maintain contact throughout a vertical circle,
    the minimum speed at the top must satisfy:

    """
)

st.latex(r"v_{top,min} = \sqrt{gr}")

st.markdown(
    "The corresponding minimum speed at the bottom is:"
)

st.latex(r"v_{bottom,min} = \sqrt{5gr}")
```

# ============================================================

# CORIOLIS EFFECT

# ============================================================

elif mode == "Coriolis Effect":

```
st.header("🌀 Coriolis Effect")

st.markdown(
    """
    The Coriolis effect appears when motion is observed from a
    rotating reference frame.

    The Coriolis acceleration is:
    """
)

st.latex(
    r"\vec{a}_C = -2\vec{\Omega} \times \vec{v}"
)

col1, col2, col3 = st.columns(3)

with col1:
    omega = st.slider(
        "Rotation rate Ω (rad/s)",
        min_value=0.0,
        max_value=10.0,
        value=2.0,
        step=0.1,
    )

with col2:
    velocity_x = st.slider(
        "Velocity x (m/s)",
        min_value=-20.0,
        max_value=20.0,
        value=5.0,
        step=0.5,
    )

with col3:
    velocity_y = st.slider(
        "Velocity y (m/s)",
        min_value=-20.0,
        max_value=20.0,
        value=0.0,
        step=0.5,
    )

velocity = np.array(
    [
        velocity_x,
        velocity_y,
        0.0,
    ]
)

omega_vector = np.array(
    [
        0.0,
        0.0,
        omega,
    ]
)

coriolis = coriolis_acceleration(
    omega_vector,
    velocity,
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Velocity magnitude",
        f"{np.linalg.norm(velocity):.2f} m/s",
    )

with col2:
    st.metric(
        "Coriolis acceleration",
        f"{np.linalg.norm(coriolis):.2f} m/s²",
    )

with col3:
    st.metric(
        "Coriolis x-component",
        f"{coriolis[0]:.2f} m/s²",
    )

st.markdown("---")

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=[0, velocity_x],
        y=[0, velocity_y],
        mode="lines+markers",
        name="Velocity",
        line=dict(width=5),
    )
)

scale = 1.0

fig.add_trace(
    go.Scatter(
        x=[
            0,
            coriolis[0] * scale,
        ],
        y=[
            0,
            coriolis[1] * scale,
        ],
        mode="lines+markers",
        name="Coriolis acceleration",
        line=dict(width=5),
    )
)

fig.update_layout(
    title="Velocity and Coriolis Acceleration",
    xaxis_title="x",
    yaxis_title="y",
    xaxis=dict(
        scaleanchor="y",
        scaleratio=1,
    ),
    height=600,
)

st.plotly_chart(
    fig,
    use_container_width=True,
)

st.subheader("Interpretation")

st.markdown(
    f"""
    The object has velocity:

    **v = ({velocity_x:.2f}, {velocity_y:.2f}) m/s**

    The calculated Coriolis acceleration is:

    **a₍C₎ = ({coriolis[0]:.2f}, {coriolis[1]:.2f}) m/s²**

    The Coriolis acceleration is perpendicular to the velocity
    when the motion is perpendicular to the rotation axis.
    """
)
```

# ============================================================

# EARTH MODE

# ============================================================

elif mode == "Earth Mode":

```
st.header("🌍 Earth Mode")

st.markdown(
    """
    Earth's rotation produces a Coriolis effect whose strength
    depends on latitude.

    The Coriolis parameter is:
    """
)

st.latex(
    r"f = 2\Omega\sin(\phi)"
)

earth_omega = earth_rotation_rate()

latitude = st.slider(
    "Latitude (degrees)",
    min_value=-90.0,
    max_value=90.0,
    value=33.6,
    step=0.1,
)

f = coriolis_parameter(
    latitude_degrees=latitude,
    earth_omega=earth_omega,
)

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Earth rotation rate",
        f"{earth_omega:.6e} rad/s",
    )

with col2:
    st.metric(
        "Coriolis parameter f",
        f"{f:.6e} s⁻¹",
    )

st.markdown("---")

latitudes = np.linspace(
    -90,
    90,
    361,
)

coriolis_values = np.array(
    [
        coriolis_parameter(
            latitude_degrees=lat,
            earth_omega=earth_omega,
        )
        for lat in latitudes
    ]
)

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=latitudes,
        y=coriolis_values,
        mode="lines",
        name="Coriolis parameter",
        line=dict(width=3),
    )
)

fig.add_trace(
    go.Scatter(
        x=[latitude],
        y=[f],
        mode="markers",
        name="Selected latitude",
        marker=dict(size=12),
    )
)

fig.add_hline(
    y=0,
    line_width=1,
)

fig.update_layout(
    title="Coriolis Parameter vs Latitude",
    xaxis_title="Latitude (degrees)",
    yaxis_title="f (s⁻¹)",
    height=600,
)

st.plotly_chart(
    fig,
    use_container_width=True,
)

st.subheader("What does this mean?")

if latitude > 0:
    hemisphere = "Northern Hemisphere"
elif latitude < 0:
    hemisphere = "Southern Hemisphere"
else:
    hemisphere = "Equator"

st.markdown(
    f"""
    **Selected location:** `{latitude:.1f}°`

    **Region:** `{hemisphere}`

    **Coriolis parameter:** `{f:.6e} s⁻¹`

    The Coriolis effect is:

    - **Zero at the equator**
    - Stronger toward the poles
    - Positive in the Northern Hemisphere
    - Negative in the Southern Hemisphere
    """
)
```

# ============================================================

# FOOTER

# ============================================================

st.markdown("---")

st.caption(
"Coriolis — The Rotating World Simulator | Computational Physics Project"
)

