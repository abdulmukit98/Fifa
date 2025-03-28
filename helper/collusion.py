import math

def check_collision(player_rect, ball_pos, ball_radius):
    # Get the closest point on the rectangle to the ball
    closest_x = max(player_rect.left, min(ball_pos[0], player_rect.right))
    closest_y = max(player_rect.top, min(ball_pos[1], player_rect.bottom))

    # Distance from closest point to the center of the ball
    distance = math.hypot(ball_pos[0] - closest_x, ball_pos[1] - closest_y)
    return distance < ball_radius 
