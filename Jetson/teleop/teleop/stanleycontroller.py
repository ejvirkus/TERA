import numpy as np

k = 0.5
Kp = 1.0
dt = 0.1
L = 1.0
max_steer = np.radians(45)

def h_err_corr(next_heading, current_heading):
    return next_heading - current_heading

def xt_err_corr(target_position, current_position, current_heading, k, v, k_s):
    v_p = target_position - current_position
    v_t = np.array([np.cos(current_heading), np.sin(current_heading)])
    xt_error = np.linalg.norm(np.cross(v_p, v_t))
    return xt_error

def steering_control(next_heading, current_heading, target_position, current_position, k, v, k_s):
    heading_err = h_err_corr(next_heading, current_heading)
    xt_err = xt_err_corr(target_position, current_position, current_heading, k, v, k_s)

    return heading_err + xt_err

def get_min_dist(current_position, x, y):
    array = np.array([[x, y] for x, y in zip(x,y)])
    distances = np.linalg.norm(array - current_position, axis=1)
    min_dist = np.argmin(distances)
    return min_dist

def implementation(gps_x, gps_y, current_x, current_y, last_x, last_y, ):
    current_position = np.array([current_x, current_y])
    nearest_point = get_min_dist(current_position, gps_x, gps_y)

    for i in range(nearest_point, len(gps_x)-1):