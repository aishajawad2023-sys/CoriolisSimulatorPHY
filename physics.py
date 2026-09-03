import numpy as np


def circular_motion(radius, omega, time):
    """
    Calculate position, velocity and centripetal acceleration
    for an object moving in a horizontal circle.
    """

    theta = omega * time

    x = radius * np.cos(theta)
    y = radius * np.sin(theta)

    vx = -radius * omega * np.sin(theta)
    vy = radius * omega * np.cos(theta)

    ax = -radius * omega**2 * np.cos(theta)
    ay = -radius * omega**2 * np.sin(theta)

    speed = abs(radius * omega)
    acceleration = radius * omega**2

    return {
        "x": x,
        "y": y,
        "vx": vx,
        "vy": vy,
        "ax": ax,
        "ay": ay,
        "speed": speed,
        "acceleration": acceleration,
    }


def vertical_circle(radius, initial_speed, g=9.81, num_points=500):
    """
    Calculate a vertical circular trajectory using conservation of energy.

    The object starts at the bottom of the circle.
    """

    theta = np.linspace(0, 2 * np.pi, num_points)

    height = radius * (1 - np.cos(theta))

    velocity_squared = initial_speed**2 - 2 * g * height

    velocity_squared = np.maximum(velocity_squared, 0)

    speed = np.sqrt(velocity_squared)

    x = radius * np.sin(theta)
    y = -radius * np.cos(theta)

    return {
        "theta": theta,
        "x": x,
        "y": y,
        "speed": speed,
        "height": height,
    }


def coriolis_acceleration(omega_vector, velocity_vector):
    """
    Calculate Coriolis acceleration:

        a_c = -2 * Omega x v
    """

    omega_vector = np.asarray(omega_vector, dtype=float)
    velocity_vector = np.asarray(velocity_vector, dtype=float)

    return -2 * np.cross(omega_vector, velocity_vector)


def coriolis_parameter(latitude_degrees, earth_omega=7.2921159e-5):
    """
    Calculate the Coriolis parameter:

        f = 2 * Omega * sin(latitude)
    """

    latitude_radians = np.radians(latitude_degrees)

    return 2 * earth_omega * np.sin(latitude_radians)


def earth_rotation_rate():
    """
    Approximate angular rotation rate of Earth in rad/s.
    """

    return 2 * np.pi / 86164


def centripetal_acceleration(radius, omega):
    """
    a = omega^2 * r
    """

    return omega**2 * radius


def centripetal_force(mass, radius, omega):
    """
    F = m * omega^2 * r
    """

    return mass * omega**2 * radius
