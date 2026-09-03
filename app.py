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


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Coriolis Physics Simulator",
    page_icon="🌍",
    layout="wide",
)


# =========================================================
# TITLE
# =========================================================

st.title("🌍 Coriolis — The Rotating World Simulator")

st.markdown(
    """
    **An interactive computational physics laboratory**

    Explore circular motion, vertical circles, rotating reference
    frames, and eventually the Coriolis effect on Earth.
    """
)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🧭 Simulation")

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

    st.write(
        "A numerical simulation of an object moving around a circle."
    )

    # -----------------------------------------------------
    # PARAMETERS
    # -----------------------------------------------------

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

        simulation_time = st.slider(
            "Simulation time (s)",
            min_value=1.0,
            max_value=30.0,
            value=10.0,
            step=1.0,
        )

    # -----------------------------------------------------
    # RUN BUTTON
    # -----------------------------------------------------

    run = st.button(
        "▶ Run simulation",
        type="primary",
    )

    # -----------------------------------------------------
    # RUN / STORE SIMULATION
    # -----------------------------------------------------

    simulation_parameters = (
        radius,
        omega,
        simulation_time,
    )

    if (
        run
        or "circular_simulation" not in st.session_state
        or st.session_state.get("circular_parameters")
        != simulation_parameters
    ):

        st.session_state.circular_simulation = (
            simulate_circular_motion(
                radius=radius,
                omega=omega,
                total_time=simulation_time,
                dt=0.01,
            )
        )

        st.session_state.circular_parameters = (
            simulation_parameters
        )

    simulation = st.session_state.circular_simulation

    positions = simulation["position"]
    velocities = simulation["velocity"]
    accelerations = simulation["acceleration"]
    times = simulation["time"]

    # -----------------------------------------------------
    # TIME CONTROL
    # -----------------------------------------------------

    current_index = st.slider(
        "Simulation time",
        min_value=0,
        max_value=len(times) - 1,
        value=0,
        step=1,
        format="Frame %d",
    )

    # Current state

    position = positions[current_index]
    velocity = velocities[current_index]
    acceleration = accelerations[current_index]

    current_time = times[current_index]

    speed = np.linalg.norm(
        velocity
    )

    acceleration_magnitude = np.linalg.norm(
        acceleration
    )

    # -----------------------------------------------------
    # METRICS
    # -----------------------------------------------------

    st.subheader("Current State")

    metric1, metric2, metric3, metric4 = st.columns(4)

    metric1.metric(
        "Time",
        f"{current_time:.2f} s",
    )

    metric2.metric(
        "Position",
        f"({position[0]:.2f}, {position[1]:.2f}) m",
    )

    metric3.metric(
        "Speed",
        f"{speed:.2f} m/s",
    )

    metric4.metric(
        "Acceleration",
        f"{acceleration_magnitude:.2f} m/s²",
    )

    # -----------------------------------------------------
    # TRAJECTORY
    # -----------------------------------------------------

    fig = go.Figure()

    # Full trajectory

    fig.add_trace(
        go.Scatter(
            x=positions[:, 0],
            y=positions[:, 1],
            mode="lines",
            name="Trajectory",
            line=dict(
                width=3,
            ),
        )
    )

    # Current particle

    fig.add_trace(
        go.Scatter(
            x=[position[0]],
            y=[position[1]],
            mode="markers",
            name="Particle",
            marker=dict(
                size=16,
            ),
        )
    )

    # -----------------------------------------------------
    # VELOCITY VECTOR
    # -----------------------------------------------------

    velocity_scale = 0.8

    velocity_end = (
        position
        + velocity * velocity_scale
    )

    fig.add_trace(
        go.Scatter(
            x=[
                position[0],
                velocity_end[0],
            ],
            y=[
                position[1],
                velocity_end[1],
            ],
            mode="lines+markers",
            name="Velocity",
            line=dict(
                width=4,
            ),
        )
    )

    # -----------------------------------------------------
    # ACCELERATION VECTOR
    # -----------------------------------------------------

    acceleration_scale = 2.0

    acceleration_end = (
        position
        + acceleration
        * acceleration_scale
    )

    fig.add_trace(
        go.Scatter(
            x=[
                position[0],
                acceleration_end[0],
            ],
            y=[
                position[1],
                acceleration_end[1],
            ],
            mode="lines+markers",
            name="Centripetal acceleration",
            line=dict(
                width=4,
            ),
        )
    )

    # -----------------------------------------------------
    # CENTER
    # -----------------------------------------------------

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

    # -----------------------------------------------------
    # GRAPH SETTINGS
    # -----------------------------------------------------

    fig.update_layout(
        title="Numerical Circular Motion",
        xaxis_title="x (m)",
        yaxis_title="y (m)",
        xaxis=dict(
            scaleanchor="y",
        ),
        height=650,
        hovermode="closest",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    # -----------------------------------------------------
    # PHYSICS
    # -----------------------------------------------------

    st.subheader("📐 Physics")

    col_a, col_b = st.columns(2)

    with col_a:

        st.latex(
            r"v = \omega r"
        )

        st.latex(
            r"a_c = \omega^2 r"
        )

    with col_b:

        theoretical_speed = (
            omega * radius
        )

        theoretical_acceleration = (
            omega**2 * radius
        )

        st.write(
            f"**Theoretical speed:** "
            f"{theoretical_speed:.4f} m/s"
        )

        st.write(
            f"**Theoretical acceleration:** "
            f"{theoretical_acceleration:.4f} m/s²"
        )

    # -----------------------------------------------------
    # EXPLANATION
    # -----------------------------------------------------

    st.info(
        """
        The velocity vector is tangent to the circular path,
        while centripetal acceleration points toward the center.
        """
    )


# =========================================================
# VERTICAL CIRCLE
# =========================================================

elif mode == "Vertical Circle":

    st.header("🟢 Vertical Circle")

    st.write(
        "Explore the motion of an object moving around a vertical loop."
    )

    # -----------------------------------------------------
    # PARAMETERS
    # -----------------------------------------------------

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

    # -----------------------------------------------------
    # PHYSICS
    # -----------------------------------------------------

    minimum_top_speed = np.sqrt(
        g * radius
    )

    minimum_bottom_speed = np.sqrt(
        5 * g * radius
    )

    data = vertical_circle(
        radius,
        initial_speed,
        g,
    )

    # -----------------------------------------------------
    # GRAPH
    # -----------------------------------------------------

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=data["x"],
            y=data["y"],
            mode="lines",
            name="Trajectory",
            line=dict(
                width=4,
            ),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=[0],
            y=[-radius],
            mode="markers",
            name="Bottom",
            marker=dict(
                size=12,
            ),
        )
    )

    fig.update_layout(
        title="Vertical Circle",
        xaxis_title="x (m)",
        yaxis_title="y (m)",
        xaxis=dict(
            scaleanchor="y",
        ),
        height=650,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    # -----------------------------------------------------
    # METRICS
    # -----------------------------------------------------

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

    # -----------------------------------------------------
    # RESULT
    # -----------------------------------------------------

    if initial_speed >= minimum_bottom_speed:

        st.success(
            "✅ The object has enough initial speed to complete the ideal loop."
        )

    else:

        st.warning(
            "⚠️ The object does not have enough initial speed for the limiting ideal loop."
        )

    # -----------------------------------------------------
    # THEORY
    # -----------------------------------------------------

    st.subheader("📐 Minimum-Speed Conditions")

    st.latex(
        r"v_{\text{top,min}} = \sqrt{gr}"
    )

    st.latex(
        r"v_{\text{bottom,min}} = \sqrt{5gr}"
    )


# =========================================================
# CORIOLIS EFFECT
# =========================================================

elif mode == "Coriolis Effect":

    st.header("🌀 Coriolis Effect")

    st.write(
        """
        Explore how motion appears inside a rotating reference frame.
        """
    )

    # -----------------------------------------------------
    # PARAMETERS
    # -----------------------------------------------------

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

    # -----------------------------------------------------
    # VELOCITY
    # -----------------------------------------------------

    angle = np.radians(
        direction
    )

    vx = speed * np.cos(angle)
    vy = speed * np.sin(angle)

    velocity_vector = np.array(
        [vx, vy, 0.0]
    )

    omega_vector = np.array(
        [0.0, 0.0, omega]
    )

    # -----------------------------------------------------
    # CORIOLIS
    # -----------------------------------------------------

    coriolis = coriolis_acceleration(
        omega_vector,
        velocity_vector,
    )

    coriolis_magnitude = np.linalg.norm(
        coriolis
    )

    # -----------------------------------------------------
    # METRICS
    # -----------------------------------------------------

    m1, m2, m3 = st.columns(3)

    m1.metric(
        "Speed",
        f"{speed:.2f} m/s",
    )

    m2.metric(
        "Rotation Ω",
        f"{omega:.2f} rad/s",
    )

    m3.metric(
        "Coriolis acceleration",
        f"{coriolis_magnitude:.3f} m/s²",
    )

    # -----------------------------------------------------
    # FORMULA
    # -----------------------------------------------------

    st.subheader("📐 Equation")

    st.latex(
        r"\vec{a}_C = -2\vec{\Omega}\times\vec{v}"
    )

    # -----------------------------------------------------
    # VECTOR GRAPH
    # -----------------------------------------------------

    scale = 2.0

    fig = go.Figure()

    # Velocity

    fig.add_trace(
        go.Scatter(
            x=[
                0,
                vx,
            ],
            y=[
                0,
                vy,
            ],
            mode="lines+markers",
            name="Velocity",
            line=dict(
                width=5,
            ),
        )
    )

    # Coriolis

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
            line=dict(
                width=5,
            ),
        )
    )

    fig.update_layout(
        title="Velocity and Coriolis Acceleration",
        xaxis_title="x",
        yaxis_title="y",
        xaxis=dict(
            scaleanchor="y",
        ),
        height=650,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    st.info(
        """
        The Coriolis acceleration is perpendicular to both the
        rotation axis and the object's velocity.
        """
    )


# =========================================================
# EARTH MODE
# =========================================================

elif mode == "Earth Mode":

    st.header("🌍 Earth Mode")

    st.write(
        """
        Investigate how Earth's rotation changes the Coriolis effect
        with latitude.
        """
    )

    # -----------------------------------------------------
    # PARAMETERS
    # -----------------------------------------------------

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

    # -----------------------------------------------------
    # EARTH ROTATION
    # -----------------------------------------------------

    omega_earth = earth_rotation_rate()

    # -----------------------------------------------------
    # CORIOLIS PARAMETER
    # -----------------------------------------------------

    f = coriolis_parameter(
        latitude,
        omega_earth,
    )

    # For motion perpendicular to Earth's rotation axis,
    # the local Coriolis acceleration magnitude is approximately
    # f * v.

    coriolis_acceleration_value = abs(
        f * object_speed
    )

    # -----------------------------------------------------
    # METRICS
    # -----------------------------------------------------

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

    # -----------------------------------------------------
    # EQUATION
    # -----------------------------------------------------

    st.subheader("📐 Coriolis Parameter")

    st.latex(
        r"f = 2\Omega\sin(\phi)"
    )

    st.write(
        f"""
        At latitude **{latitude:.0f}°**:

        **f = {f:.6e} s⁻¹**
        """
    )

    # -----------------------------------------------------
    # LATITUDE GRAPH
    # -----------------------------------------------------

    latitudes = np.linspace(
        -90,
        90,
        361,
    )

    f_values = np.array(
        [
            coriolis_parameter(
                lat,
                omega_earth,
            )
            for lat in latitudes
        ]
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=latitudes,
            y=f_values,
            mode="lines",
            name="Coriolis parameter",
            line=dict(
                width=4,
            ),
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
        height=550,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    # -----------------------------------------------------
    # EXPLANATION
    # -----------------------------------------------------

    st.info(
        """
        At the equator, the Coriolis parameter is zero.
        Its magnitude increases toward the poles.
        """
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "Coriolis — The Rotating World Simulator | "
    "Computational Physics Project"
)

