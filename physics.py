import numpy as np


# ============================================================
# CIRCULAR MOTION
# ============================================================

def simulate_circular_motion(
    radius,
    omega,
    total_time,
    dt=0.01,
):
    """
    Simulate uniform circular motion.

    Parameters
    ----------
    radius : float
        Radius of the circular path in meters.

    omega : float
        Angular velocity in radians per second.

    total_time : float
        Total simulation time in seconds.

    dt : float
        Time step in seconds.

    Returns
    -------
    times : numpy.ndarray
        Simulation time values.

    positions : numpy.ndarray
        x and y positions at each time.

    velocities : numpy.ndarray
        x and y velocities at each time.
    """

    times = np.arange(
        0.0,
        total_time + dt,
        dt,
    )

    # Position:
    # x = r cos(ωt)
    # y = r sin(ωt)

    x = radius * np.cos(omega * times)
    y = radius * np.sin(omega * times)

    positions = np.column_stack(
        (x, y)
    )

    # Velocity:
    # vx = -rω sin(ωt)
    # vy =  rω cos(ωt)

    vx = -radius * omega * np.sin(omega * times)
    vy = radius * omega * np.cos(omega * times)

    velocities = np.column_stack(
        (vx, vy)
    )

    return times, positions, velocities


# ============================================================
# VERTICAL CIRCLE
# ============================================================

def vertical_circle(
    radius,
    gravity,
    num_points=361,
):
    """
    Calculate a vertical circular path.

    Returns the angle, x position, y position,
    and speed required for the minimum-contact
    vertical-circle condition.
    """

    theta = np.linspace(
        0.0,
        2.0 * np.pi,
        num_points,
    )

    x = radius * np.cos(theta)
    y = radius * np.sin(theta)

    # Minimum-contact condition at the top:
    #
    # v_top^2 = g r
    #
    # Using conservation of energy:
    #
    # v^2 = v_top^2 + 2gr(1 - sin(theta))

    v_top_squared = gravity * radius

    velocity_squared = (
        v_top_squared
        + 2.0 * gravity * radius * (1.0 - np.sin(theta))
    )

    velocity_squared = np.maximum(
        velocity_squared,
        0.0,
    )

    velocity = np.sqrt(
        velocity_squared
    )

    return theta, x, y, velocity


# ============================================================
# CORIOLIS ACCELERATION
# ============================================================

def coriolis_acceleration(
    omega_vector,
    velocity,
):
    """
    Calculate Coriolis acceleration.

    Formula:

        a_c = -2 (Ω × v)

    Parameters
    ----------
    omega_vector : array-like
        Rotation vector Ω.

    velocity : array-like
        Velocity vector v.

    Returns
    -------
    numpy.ndarray
        Coriolis acceleration vector.
    """

    omega_vector = np.asarray(
        omega_vector,
        dtype=float,
    )

    velocity = np.asarray(
        velocity,
        dtype=float,
    )

    return -2.0 * np.cross(
        omega_vector,
        velocity,
    )


# ============================================================
# CORIOLIS PARAMETER
# ============================================================

def coriolis_parameter(
    latitude_degrees,
    earth_omega=None,
):
    """
    Calculate the Coriolis parameter.

    Formula:

        f = 2 Ω sin(latitude)

    Parameters
    ----------
    latitude_degrees : float
        Latitude in degrees.

    earth_omega : float, optional
        Earth's angular rotation rate.

    Returns
    -------
    float
        Coriolis parameter in s^-1.
    """

    if earth_omega is None:
        earth_omega = earth_rotation_rate()

    latitude_radians = np.radians(
        latitude_degrees
    )

    return (
        2.0
        * earth_omega
        * np.sin(latitude_radians)
    )


# ============================================================
# EARTH ROTATION RATE
# ============================================================

def earth_rotation_rate():
    """
    Return Earth's angular rotation rate.

    One sidereal rotation is approximately
    23 hours, 56 minutes, 4 seconds.
    """

    sidereal_day = (
        23.0 * 3600.0
        + 56.0 * 60.0
        + 4.0
    )

    return (
        2.0 * np.pi
        / sidereal_day
    )
