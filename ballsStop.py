import random
import pygame
import sys
import math

pygame.init()

clock = pygame.time.Clock()

DAMPING = 0.99

class Ball:
    def __init__(self, x, y, speed, color):
        self.x = x
        self.y = y
        self.speed_x = speed
        self.speed_y = speed
        self.color = color

aux = int(input("How many balls do you want to create? "))

screen = pygame.display.set_mode((800, 600))
balls = []

RADIUS = 30

for i in range(aux):
    while True:
        x = random.randrange(RADIUS, 800 - RADIUS)
        y = random.randrange(RADIUS, 600 - RADIUS)
        flag_repeat = False
        for ball in balls:
            distance = ((x - ball.x) ** 2 + (y - ball.y) ** 2) ** 0.5
            if distance <= 2 * RADIUS: 
                flag_repeat = True
                break
        if not flag_repeat:
            break

    speed = random.randrange(-4, 5)
    color = (random.randrange(0, 256), random.randrange(0, 256), random.randrange(0, 256))
    balls.append(Ball(x, y, speed, color))

while True:
    screen.fill((0, 0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos  
            for ball in balls:
                if (ball.x - pos[0]) ** 2 + (ball.y - pos[1]) ** 2 <= RADIUS ** 2:
                    dx = ball.x - pos[0]
                    dy = ball.y - pos[1]
                    norm = math.hypot(dx, dy)
                    if norm == 0:
                        norm = 1
                    impulse = 5
                    ball.speed_x = (dx / norm) * impulse
                    ball.speed_y = (dy / norm) * impulse

    for i in range(aux):
        pygame.draw.circle(screen, balls[i].color, (int(balls[i].x), int(balls[i].y)), RADIUS)
        
        balls[i].x += balls[i].speed_x
        balls[i].y += balls[i].speed_y

        if balls[i].x > 800 - RADIUS or balls[i].x < RADIUS:
            balls[i].speed_x *= -1
        if balls[i].y > 600 - RADIUS or balls[i].y < RADIUS:
            balls[i].speed_y *= -1

        for j in range(aux):
            if i != j:
                dx = balls[i].x - balls[j].x
                dy = balls[i].y - balls[j].y
                distance_square = dx * dx + dy * dy
                distance = math.sqrt(distance_square)
                if distance < 2 * RADIUS:
                    dot = ((balls[i].speed_x - balls[j].speed_x) * dx + (balls[i].speed_y - balls[j].speed_y) * dy)
                    if distance_square != 0:
                        factor = dot / distance_square
                    else:
                        factor = 0
                    ball1_dvx = factor * dx
                    ball1_dvy = factor * dy
                    ball2_dvx = factor * (-dx)
                    ball2_dvy = factor * (-dy)
                    
                    balls[i].speed_x -= ball1_dvx
                    balls[i].speed_y -= ball1_dvy
                    balls[j].speed_x -= ball2_dvx
                    balls[j].speed_y -= ball2_dvy
        
        balls[i].speed_x *= DAMPING
        balls[i].speed_y *= DAMPING

    pygame.display.update()
    clock.tick(120)
