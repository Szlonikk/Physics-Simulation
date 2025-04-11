import random
import pygame
import sys

pygame.init()

clock = pygame.time.Clock()

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


i = 0

for i in range(aux):

    
    while(True):
        x = random.randrange(30, 770)
        y = random.randrange(30, 570)
        j=0
        flag_repeat = False
        for j in range(i):
            distance_square = ((x - balls[j].x) ** 2 + (y - balls[j].y) ** 2) ** 0.5
            if distance_square <= 60:
                flag_repeat = True
                break
        if flag_repeat == False:
            break
    
    speed = random.randrange(-4, 4)
    color = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
    balls.append(Ball(x, y, speed, color))

while True:

    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    for i in range(aux):

        pygame.draw.circle(screen, balls[i].color, (balls[i].x, balls[i].y), 30)

        balls[i].x += balls[i].speed_x
        balls[i].y += balls[i].speed_y

        if balls[i].x > 800 - 30 or balls[i].x < 30:
            balls[i].speed_x *= -1
        if balls[i].y > 600 - 30 or balls[i].y < 30:
            balls[i].speed_y *= -1
        j = 0
        for j in range(aux):
            if i != j:

                distance_square = (balls[i].x - balls[j].x) ** 2 + (balls[i].y - balls[j].y) ** 2
                distance = distance_square ** 0.5
                if (distance < 60):

                    ball1_dvx = ((balls[i].speed_x - balls[j].speed_x) * (balls[i].x - balls[j].x) + (balls[i].speed_y - balls[j].speed_y) * (balls[i].y - balls[j].y)) * (balls[i].x - balls[j].x) / distance_square
                    ball1_dvy = ((balls[i].speed_x - balls[j].speed_x) * (balls[i].x - balls[j].x) + (balls[i].speed_y - balls[j].speed_y) * (balls[i].y - balls[j].y)) * (balls[i].y - balls[j].y) / distance_square
                    ball2_dvx = ((balls[j].speed_x - balls[i].speed_x) * (balls[j].x - balls[i].x) + (balls[j].speed_y - balls[i].speed_y) * (balls[j].y - balls[i].y)) * (balls[j].x - balls[i].x) / distance_square
                    ball2_dvy = ((balls[j].speed_x - balls[i].speed_x) * (balls[j].x - balls[i].x) + (balls[j].speed_y - balls[i].speed_y) * (balls[j].y - balls[i].y)) * (balls[j].y - balls[i].y) / distance_square

                    balls[i].speed_x -= ball1_dvx
                    balls[i].speed_y -= ball1_dvy
                    balls[j].speed_x -= ball2_dvx
                    balls[j].speed_y -= ball2_dvy

    pygame.display.update()

    clock.tick(120)