import streamlit as st
import numpy as np
import plotly.graph_objects as go

from physics import (
    circular_motion,
    vertical_circle,
    coriolis_acceleration,
    coriolis_parameter,
    earth_rotation_rate,
    centripetal_acceleration,
    centripetal_force,
)


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="Coriolis Physics Simulator",
    page_icon="🌍",
    layout="wide",
)


# ---------------------------------------------------------
# TITLE
# ---------------------------------------------------------

st.title("🌍 Coriolis — The Rotating World Simulator")

st.markdown(
    """
    An interactive computational physics laboratory for exploring
    circular motion, rotating reference frames and the Coriolis effect.
    """
)


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

st.sidebar.header("Simulation")

mode = st.sidebar.selectbox(
    "Choose a simulation",
    [
        "Circular Motion",
        "Vertical Circle",
        "Coriolis Effect",
        "Earth Mode",
    ],
)


# =========================================================
# CIRCULAR MOTION
# =========================================================

if mode == "Circular Motion":

    st.header("🔵 Circular Motion")

    col1, col2, col3 = st.columns(3)

    with col1:
        radius = st.slider(
            "Radius (m)",
            min_value=1.0,
            max_value=100.0,
            value=20.0,
            step=1.0,
        )

    with col2:
        omega = st.slider(
            "Angular velocity (rad/s)",
            min_value=0.1,
            max_value=10.0,
            value=2.0,
            step=0.1,
        )

    with col3:
        time = st.slider(
            "Time (s)",
            min_value=0.0,
            max_value=20.0,
            value=1.0,
            step=0.1,
        )

    result = circular_motion(radius, omega, time)

    speed = result["speed"]
    acceleration = result["acceleration"]

    # -----------------------------------------------------
    # Metrics
    # -----------------------------------------------------

    m1, m2, m3 = st.columns(3)

    m1.metric(
        "Radius",
        f"{radius:.2f} m",
    )

    m2.metric(
        "Linear speed",
        f"{speed:.2f} m/s",
    )

    m3.metric(
        "Centripetal acceleration",
        f"{acceleration:.2f} m/s²",
    )

    # -----------------------------------------------------
    # Circle
    # -----------------------------------------------------

    angles = np.linspace(0, 2 * np.pi, 400)

    circle_x = radius * np.cos(angles)
    circle_y = radius * np.sin(angles)

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=circle_x,
            y=circle_y,
            mode="lines",
            name="Circular path",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=[result["x"]],
            y=[result["y"]],
            mode="markers",
            marker=dict(size=15),
            name="Particle",
        )
    )

    # Radius vector

    fig.add_trace(
        go.Scatter(
            x=[0, result["x"]],
            y=[0, result["y"]],
            mode="lines",
            name="Position vector",
        )
    )

    # Velocity vector

    velocity_scale = radius * 0.35

    vx_end = result["x"] + result["vx"] / speed * velocity_scale
    vy_end = result["y"] + result["vy"] / speed * velocity_scale

    fig.add_trace(
        go.Scatter(
            x=[result["x"], vx_end],
            y=[result["y"], vy_end],
            mode="lines+markers",
            name="Velocity",
        )
    )

    # Acceleration vector

    acceleration_scale = radius * 0.35

    acceleration_magnitude = np.sqrt(
        result["ax"] ** 2 + result["ay"] ** 2
    )

    ax_end = (
        result["x"]
        + result["ax"] / acceleration_magnitude * acceleration_scale
    )

    ay_end = (
        result["y"]
        + result["ay"] / acceleration_magnitude * acceleration_scale
    )

    fig.add_trace(
        go.Scatter(
            x=[result["x"], ax_end],
            y=[result["y"], ay_end],
            mode="lines+markers",
            name="Centripetal acceleration",
        )
    )

    fig.update_layout(
        title="Circular Motion",
        xaxis_title="x (m)",
        yaxis_title="y (m)",
        xaxis=dict(scaleanchor="y"),
        height=600,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    st.subheader("Physics")

    st.latex(r"v = \omega r")

    st.latex(r"a_c = \omega^2 r")

    st.markdown(
        f"""
        **Current values**

        - Radius: `{radius:.2f} m`
        - Angular velocity: `{omega:.2f} rad/s`
        - Linear speed: `{speed:.2f} m/s`
        - Centripetal acceleration: `{acceleration:.2f} m/s²`
        """
    )


# =========================================================
# VERTICAL CIRCLE
# =========================================================

elif mode == "Vertical Circle":

    st.header("🟢 Vertical Circle")

    radius = st.slider(
        "Radius (m)",
        min_value=1.0,
        max_value=50.0,
        value=10.0,
        step=1.0,
    )

    initial_speed = st.slider(
        "Initial speed at bottom (m/s)",
        min_value=1.0,
        max_value=50.0,
        value=15.0,
        step=0.5,
    )

    g = 9.81

    minimum_top_speed = np.sqrt(g * radius)

    minimum_bottom_speed = np.sqrt(5 * g * radius)

    data = vertical_circle(
        radius,
        initial_speed,
        g,
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=data["x"],
            y=data["y"],
            mode="lines",
            name="Trajectory",
        )
    )

    fig.update_layout(
        title="Vertical Circle",
        xaxis_title="x (m)",
        yaxis_title="y (m)",
        xaxis=dict(scaleanchor="y"),
        height=600,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Initial speed",
        f"{initial_speed:.2f} m/s",
    )

    c2.metric(
        "Minimum top speed",
        f"{minimum_top_speed:.2f} m/s",
    )

    c3.metric(
        "Minimum bottom speed",
        f"{minimum_bottom_speed:.2f} m/s",
    )

    if initial_speed >= minimum_bottom_speed:
        st.success(
            "The object has enough initial speed to complete the ideal loop."
        )
    else:
        st.warning(
            "The object does not have enough initial speed for the limiting ideal loop."
        )

    st.subheader("Minimum-speed condition")

    st.latex(r"v_{\text{top,min}} = \sqrt{gr}")

    st.latex(r"v_{\text{bottom,min}} = \sqrt{5gr}")


# =========================================================
# CORIOLIS EFFECT
# =========================================================

elif mode == "Coriolis Effect":

    st.header("🌀 Coriolis Effect")

    st.write(
        "Explore how apparent acceleration changes inside a rotating reference frame."
    )

    col1, col2 = st.columns(2)

    with col1:

        omega = st.slider(
            "Rotation rate Ω (rad/s)",
            min_value=0.0,
            max_value=5.0,
            value=1.0,
            step=0.1,
        )

    with col2:

        speed = st.slider(
            "Object speed (m/s)",
            min_value=0.1,
            max_value=50.0,
            value=10.0,
            step=0.5,
        )

    direction = st.slider(
        "Velocity direction (degrees)",
        min_value=0,
        max_value=360,
        value=0,
        step=5,
    )

    angle = np.radians(direction)

    vx = speed * np.cos(angle)
    vy = speed * np.sin(angle)

    omega_vector = np.array([0.0, 0.0, omega])

    velocity_vector = np.array(
        [vx, vy, 0.0]
    )

    coriolis = coriolis_acceleration(
        omega_vector,
        velocity_vector,
    )

    coriolis_magnitude = np.linalg.norm(
        coriolis
    )

    st.metric(
        "Coriolis acceleration",
        f"{coriolis_magnitude:.3f} m/s²",
    )

    st.latex(
        r"\vec{a}_C = -2\vec{\Omega}\times\vec{v}"
    )

    # -----------------------------------------------------
    # Vector visualization
    # -----------------------------------------------------

    scale = 2.0

    fig = go.Figure()

    # Velocity vector

    fig.add_trace(
        go.Scatter(
            x=[0, vx],
            y=[0, vy],
            mode="lines+markers",
            name="Velocity",
        )
    )

    # Coriolis vector

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
        )
    )

    fig.update_layout(
        title="Velocity and Coriolis Acceleration",
        xaxis_title="x",
        yaxis_title="y",
        xaxis=dict(scaleanchor="y"),
        height=600,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )


# =========================================================
# EARTH MODE
# =========================================================

elif mode == "Earth Mode":

    st.header("🌍 Earth Mode")

    latitude = st.slider(
        "Latitude (degrees)",
        min_value=-90.0,
        max_value=90.0,
        value=45.0,
        step=1.0,
    )

    object_speed = st.slider(
        "Object speed (m/s)",
        min_value=1.0,
        max_value=1000.0,
        value=100.0,
        step=10.0,
    )

    omega_earth = earth_rotation_rate()

    f = coriolis_parameter(
        latitude,
        omega_earth,
    )

    coriolis_acceleration_value = abs(
        f * object_speed
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Latitude",
        f"{latitude:.0f}°",
    )

    c2.metric(
        "Earth rotation rate",
        f"{omega_earth:.6e} rad/s",
    )

    c3.metric(
        "Coriolis acceleration",
        f"{coriolis_acceleration_value:.6f} m/s²",
    )

    st.subheader("Coriolis parameter")

    st.latex(
        r"f = 2\Omega\sin(\phi)"
    )

    st.write(
        f"For latitude **{latitude:.0f}°**, "
        f"the Coriolis parameter is approximately "
        f"**{f:.6e} s⁻¹**."
    )

    # -----------------------------------------------------
    # Latitude graph
    # -----------------------------------------------------

    latitudes = np.linspace(
        -90,
        90,
        361,
    )

    f_values = [
        coriolis_parameter(
            lat,
            omega_earth,
        )
        for lat in latitudes
    ]

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=latitudes,
            y=f_values,
            mode="lines",
            name="Coriolis parameter",
        )
    )

    fig.add_vline(
        x=latitude,
        line_dash="dash",
    )

    fig.update_layout(
        title="Coriolis Parameter vs Latitude",
        xaxis_title="Latitude (degrees)",
        yaxis_title="f (s⁻¹)",
        height=500,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    st.info(
        "The Coriolis effect is zero at the equator and has maximum magnitude near the poles."
    )
