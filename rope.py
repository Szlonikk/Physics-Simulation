import pygame
import sys
import math

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Symulacja liny z particle'ami - przeciąganie myszką")

clock = pygame.time.Clock()

class Particle:
    def __init__(self, x, y, pinned=False):
        self.pos = pygame.Vector2(x, y)       
        self.old_pos = pygame.Vector2(x, y)   
        self.acceleration = pygame.Vector2(0, 0)
        self.pinned = pinned                
    def apply_force(self, force):
        self.acceleration += force
    
    def update(self, dt):
        if self.pinned:
            return
        
        velocity = self.pos - self.old_pos
        temp = self.pos.copy()
        self.pos = self.pos + velocity + self.acceleration * (dt ** 2)
        self.old_pos = temp
        
        self.acceleration = pygame.Vector2(0, 0)

class Rope:
    def __init__(self, start_x, start_y, num_particles, spacing):
        self.particles = []
        self.segment_length = spacing
        
        for i in range(num_particles):
            pinned = (i == 0)
            particle = Particle(start_x + i * spacing, start_y, pinned=pinned)
            self.particles.append(particle)
        
        self.num_constraint_iterations = 10

    def update(self, dt):
        gravity = pygame.Vector2(0, 0.5)
        for particle in self.particles:
            particle.apply_force(gravity)
            particle.update(dt)
        
        self.apply_constraints()
    
    def apply_constraints(self):
        for _ in range(self.num_constraint_iterations):
            for i in range(len(self.particles) - 1):
                p1 = self.particles[i]
                p2 = self.particles[i + 1]
                delta = p2.pos - p1.pos
                distance = delta.length()
                if distance == 0:
                    continue  
                difference = (distance - self.segment_length) / distance
                correction = delta * 0.5 * difference
                if not p1.pinned:
                    p1.pos += correction
                if not p2.pinned:
                    p2.pos -= correction

    def draw(self, surface):
        for i in range(len(self.particles) - 1):
            start = (int(self.particles[i].pos.x), int(self.particles[i].pos.y))
            end = (int(self.particles[i+1].pos.x), int(self.particles[i+1].pos.y))
            pygame.draw.line(surface, (255, 255, 255), start, end, 2)
        
        for particle in self.particles:
            pos_int = (int(particle.pos.x), int(particle.pos.y))
            pygame.draw.circle(surface, (255, 0, 0), pos_int, 5)

start_x = 100
start_y = 100
num_particles = 20
spacing = 20

rope = Rope(start_x, start_y, num_particles, spacing)

dragged_particle = None
drag_threshold = 10  

running = True
while running:
    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
            for particle in rope.particles:
                if (particle.pos - mouse_pos).length() < drag_threshold:
                    dragged_particle = particle
                    dragged_particle.old_pos = mouse_pos.copy()
                    dragged_particle.pos = mouse_pos.copy()
                    break
        
        elif event.type == pygame.MOUSEBUTTONUP:
            dragged_particle = None
        
        elif event.type == pygame.MOUSEMOTION:
            if dragged_particle:
                mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
                dragged_particle.pos = mouse_pos.copy()
                dragged_particle.old_pos = mouse_pos.copy()  
    
    rope.update(dt)
    
    screen.fill((0, 0, 0))
    
    rope.draw(screen)
    
    pygame.display.flip()

pygame.quit()
sys.exit()
