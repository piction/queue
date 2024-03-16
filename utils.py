import numpy as np

def are_points_on_same_line(point1, point2, point3):
    # Calculate the slopes of the lines formed by pairs of points
    slope1 = (
        (point2[1] - point1[1]) / (point2[0] - point1[0])
        if point2[0] != point1[0]
        else None
    )
    slope2 = (
        (point3[1] - point2[1]) / (point3[0] - point2[0])
        if point3[0] != point2[0]
        else None
    )
    slope3 = (
        (point3[1] - point1[1]) / (point3[0] - point1[0])
        if point3[0] != point1[0]
        else None
    )

    # Check if all slopes are equal (or if all are None, indicating vertical lines)
    exact_on_line = slope1 == slope2 == slope3
    if exact_on_line:
        return True
    if slope1 is None or slope2 is None or slope3 is None:
        return False
    return (
        abs(slope1 - slope2) < 0.001
        and abs(slope2 - slope3) < 0.001
        and abs(slope1 - slope3) < 0.001
    )


def removeIntermediatePathPoints(points):
    if len(points) <= 2:
        return
    filtered_points = [points[0]]
    for i, p in enumerate(points[1:-2]):
        # check if midpoint is on line of previous and next point assume
        if not are_points_on_same_line(filtered_points[-1], p, points[i + 2]):
            filtered_points.append(p)
    filtered_points.append(points[-1])
    points = filtered_points



def velocity_profile(distance, max_velocity, acceleration):
    """
    Creates a velocity profile for motion along a straight line with fixed acceleration,
    maximum velocity, and deceleration equal to the acceleration.

    Parameters:
        distance (float): Total distance to be covered.
        max_velocity (float): Maximum velocity allowed.
        acceleration (float): Acceleration and deceleration magnitude.

    Returns:
        tuple: Tuple containing arrays for time and velocity.
    """
    # Calculate time to reach max velocity (t1)
    t1 = max_velocity / acceleration

    # Calculate distance covered during acceleration phase (d1)
    d1 = 0.5 * acceleration * t1 ** 2

    # If distance is less than 2*d1, we can't reach max velocity
    if distance < 2 * d1:
        # Adjust max velocity
        max_velocity = (distance * acceleration) ** 0.5
        t1 = max_velocity / acceleration
        d1 = 0.5 * acceleration * t1 ** 2

    # Calculate time taken to cover distance during acceleration and deceleration phase (t2)
    t2 = (distance - 2 * d1) / max_velocity

    # Calculate total time (t_total)
    t_total = 2*t1 + t2

    # Create time array from 0 to t_total
    time = np.linspace(0, t_total, 1000)
    print(max_velocity)
    # Create velocity profile
    velocity = np.piecewise(time,
                             [time < t1, (time >= t1) & (time <= t_total - t1), time > t_total - t1],
                             [lambda t: acceleration * t,
                              max_velocity,
                              lambda t: max_velocity - acceleration * (t - (t_total - t1))]
                             )

    return time, velocity
