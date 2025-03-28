import pygame
from helper.collusion import check_collision

pygame.init()

# Screen
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini FIFA")


# Colors
GREEN = (34, 139, 34)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

player = pygame.Rect(100, 100, 40, 60)
ai_player = pygame.Rect(WIDTH - 200, HEIGHT // 2, 40, 60)
ball_pos = [300, 300]
ball_radius = 15

ball_velocity = [0, 0]
FRICTION = 0.95

GOAL_WIDTH = 10
GOAL_HEIGHT = 200
GOAL_Y = (HEIGHT - GOAL_HEIGHT) // 2
left_goal = pygame.Rect(0, GOAL_Y, GOAL_WIDTH, GOAL_HEIGHT)
right_goal = pygame.Rect(WIDTH - GOAL_WIDTH, GOAL_Y, GOAL_WIDTH, GOAL_HEIGHT)
  
your_score = 0
ai_score = 0
font = pygame.font.SysFont(None, 60)

# Game loop
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= 5
    if keys[pygame.K_RIGHT]:
        player.x +=5
    if keys[pygame.K_UP]:
        player.y -= 5
    if keys[pygame.K_DOWN]:
        player.y += 5


    if check_collision(player, ball_pos, ball_radius):
        if keys[pygame.K_LEFT]:
            ball_velocity[0] -=10
        if keys[pygame.K_RIGHT]:
            ball_velocity[0] += 10
        if keys[pygame.K_UP]:
            ball_velocity[1] -= 10
        if keys[pygame.K_DOWN]:
            ball_velocity[1] += 10

    # update ball position
    ball_pos[0] += ball_velocity[0]
    ball_pos[1] += ball_velocity[1]

    # Apply Friction
    ball_velocity[0] *= FRICTION
    ball_velocity[1] *= FRICTION


    screen.fill(GREEN)
    pygame.draw.rect(screen, BLUE, player)
    ball = pygame.draw.circle(screen, WHITE, ball_pos, ball_radius)
    # Left goal ME
    pygame.draw.rect(screen, (255, 0, 0), left_goal)
    # Right GOal AI
    pygame.draw.rect(screen, (0, 0, 255), right_goal)
    pygame.draw.rect(screen, (255, 0, 0), ai_player)

    # GOAL
    if ball.colliderect(left_goal):
        ai_score += 1
        print("GOAL! AI scored!")
        ball_pos = [WIDTH // 2, HEIGHT // 2]
        ball_velocity = [0, 0]
    
    if ball.colliderect(right_goal):
        your_score += 1
        print("GOAL! You scored!")
        ball_pos = [WIDTH // 2, HEIGHT // 2]
        ball_velocity = [0, 0]

    # AI kick ball
    if check_collision(ai_player, ball_pos, ball_radius):
        ball_velocity[0] = -10

    # Smart AI in x direction
    if ball_pos[0] > WIDTH // 2:
        if ball_pos[0] < ai_player.centerx:
            ai_player.x -= 2
        elif ball_pos[0] > ai_player.centerx:
            ai_player.x += 2

        # move ai player vertically when ball in 2nd quadrant
        if ball_pos[1] < ai_player.centery:
            ai_player.y -= 2
        elif ball_pos[1] > ai_player.centery:
            ai_player.y += 2

    # Return Previous pos
    else:
        if ai_player.centerx < WIDTH - 200:
            ai_player.x += 2
        elif ai_player.centerx > WIDTH - 200:
            ai_player.x -= 2

    # Keep ball inside the edge    
    if ball_pos[0] + ball_radius > WIDTH:
        ball_pos[0] = WIDTH - ball_radius
        ball_velocity[0] *= -0.5
    
    if ball_pos[0] - ball_radius < 0:
        ball_pos[0] = ball_radius
        ball_velocity[0] *= -0.5     # change ball direction
    
    if ball_pos[1] - ball_radius < 0:
        ball_pos[1] = ball_radius
        ball_velocity[1] *= -0.5
    
    if ball_pos[1] + ball_radius > HEIGHT:
        ball_pos[1] = HEIGHT - ball_radius
        ball_velocity[1] *= -0.5
    
    score_text = font.render(f"You: {your_score}  AI: {ai_score}", True, (0, 0, 0))
    screen.blit(score_text, (WIDTH //2 - score_text.get_width() // 2, 20))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

