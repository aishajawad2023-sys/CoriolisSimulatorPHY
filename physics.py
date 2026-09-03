import numpy as np


def acceleration_circular(position, omega):
    """
    Centripetal acceleration for an object constrained
    to circular motion.

    a = -omega^2 * r
    """

    return -omega**2 * position


def simulate_particle(
    initial_position,
    initial_velocity,
    acceleration_function,
    total_time=10.0,
    dt=0.01,
):
    """
    Generic numerical particle simulator.

    Uses simple Euler integration.

    Parameters
    ----------
    initial_position : array-like
        Starting position [x, y]

    initial_velocity : array-like
        Starting velocity [vx, vy]

    acceleration_function : function
        Function receiving (position, velocity, time)
        and returning acceleration [ax, ay]

    total_time : float
        Simulation duration in seconds

    dt : float
        Simulation timestep
    """

    steps = int(total_time / dt) + 1

    times = np.linspace(
        0,
        total_time,
        steps,
    )

    positions = np.zeros(
        (steps, 2)
    )

    velocities = np.zeros(
        (steps, 2)
    )

    accelerations = np.zeros(
        (steps, 2)
    )

    positions[0] = np.asarray(
        initial_position,
        dtype=float,
    )

    velocities[0] = np.asarray(
        initial_velocity,
        dtype=float,
    )

    for i in range(steps - 1):

        t = times[i]

        acceleration = acceleration_function(
            positions[i],
            velocities[i],
            t,
        )

        accelerations[i] = acceleration

        velocities[i + 1] = (
            velocities[i]
            + acceleration * dt
        )

        positions[i + 1] = (
            positions[i]
            + velocities[i + 1] * dt
        )

    accelerations[-1] = acceleration_function(
        positions[-1],
        velocities[-1],
        times[-1],
    )

    return {
        "time": times,
        "position": positions,
        "velocity": velocities,
        "acceleration": accelerations,
    }


def simulate_circular_motion(
    radius=20.0,
    omega=2.0,
    total_time=10.0,
    dt=0.01,
):
    """
    Numerically simulate circular motion.

    The object starts at:
        x = radius
        y = 0

    and has initial tangential velocity.
    """

    initial_position = np.array(
        [radius, 0.0]
    )

    initial_velocity = np.array(
        [0.0, radius * omega]
    )

    def acceleration(
        position,
        velocity,
        time,
    ):
        return acceleration_circular(
            position,
            omega,
        )

    return simulate_particle(
        initial_position,
        initial_velocity,
        acceleration,
        total_time,
        dt,
    )


def coriolis_acceleration(
    omega_vector,
    velocity_vector,
):
    """
    Coriolis acceleration:

        a_c = -2 Ω × v
    """

    omega_vector = np.asarray(
        omega_vector,
        dtype=float,
    )

    velocity_vector = np.asarray(
        velocity_vector,
        dtype=float,
    )

    return -2 * np.cross(
        omega_vector,
        velocity_vector,
    )


def coriolis_parameter(
    latitude_degrees,
    earth_omega=7.2921159e-5,
):
    """
    Coriolis parameter:

        f = 2 Ω sin(latitude)
    """

    latitude_radians = np.radians(
        latitude_degrees
    )

    return (
        2
        * earth_omega
        * np.sin(latitude_radians)
    )


def earth_rotation_rate():
    """
    Earth's approximate sidereal
    rotation rate in rad/s.
    """

    return 2 * np.pi / 86164


def centripetal_acceleration(
    radius,
    omega,
):
    return omega**2 * radius


def centripetal_force(
    mass,
    radius,
    omega,
):
    return mass * omega**2 * radius
