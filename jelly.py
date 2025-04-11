import pygame
import math

WIDTH, HEIGHT = 800, 600
FPS = 60
GRAVITY = 9.81  
GROUND_Y = HEIGHT - 50  

class Node:
    def __init__(self, x, y, mass=1):
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(0, 0)
        self.force = pygame.Vector2(0, 0)
        self.mass = mass

    def update(self, dt):
        acc = self.force / self.mass
        self.vel += acc * dt
        self.pos += self.vel * dt
        self.force = pygame.Vector2(0, 0)

class Spring:
    def __init__(self, node_a, node_b, rest_length, k, damping=0.1):
        self.a = node_a
        self.b = node_b
        self.rest_length = rest_length
        self.k = k  
        self.damping = damping  

    def apply(self):
        vec = self.b.pos - self.a.pos
        length = vec.length()
        if length != 0:
            direction = vec / length
            force = self.k * (length - self.rest_length)
            relative_velocity = (self.b.vel - self.a.vel).dot(direction)
            damping_force = self.damping * relative_velocity
            total_force = (force + damping_force) * direction
            self.a.force += total_force
            self.b.force -= total_force

class Gummy:
    def __init__(self, center, radius, num_points, k_perimeter, k_center, damping):
        self.nodes = []
        self.springs = []

        self.center = Node(center[0], center[1])
        self.nodes.append(self.center)

        angle_step = 2 * math.pi / num_points
        for i in range(num_points):
            angle = i * angle_step
            x = center[0] + radius * math.cos(angle)
            y = center[1] + radius * math.sin(angle)
            self.nodes.append(Node(x, y))
        
        for i in range(1, num_points + 1):
            rest_length = radius
            self.springs.append(Spring(self.center, self.nodes[i], rest_length, k_center, damping))
        
        for i in range(1, num_points + 1):
            a = self.nodes[i]
            b = self.nodes[1 + (i % num_points)]
            rest_length = 2 * radius * math.sin(math.pi / num_points)
            self.springs.append(Spring(a, b, rest_length, k_perimeter, damping))
        

    def update(self, dt):
        for spring in self.springs:
            spring.apply()
        for node in self.nodes:
            node.force += pygame.Vector2(0, GRAVITY * node.mass * 20)  # Skalowanie grawitacji – dopasować do okna
            node.update(dt)
            if node.pos.y > GROUND_Y:
                node.pos.y = GROUND_Y
                if node.vel.y > 0:
                    node.vel.y *= -0.3  # zmienną tę można dostroić
                    node.vel.x *= 0.9

    def draw(self, screen):
        for spring in self.springs:
            pygame.draw.line(screen, (255, 0, 0), spring.a.pos, spring.b.pos, 2)
        for node in self.nodes:
            pygame.draw.circle(screen, (0, 255, 0), (int(node.pos.x), int(node.pos.y)), 5)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Symulacja fizyczna żelka")
    clock = pygame.time.Clock()

    # center – początkowa pozycja żelka,
    # radius – promień okręgu, na którym rozlokowane są węzły obwodowe,
    # num_points – liczba punktów obwodowych,
    # k_perimeter – stała sprężystości dla sprężyn obwodowych,
    # k_center – stała sprężystości dla sprężyn łączących środek z obwodem,
    # damping – współczynnik tłumienia.
    gummy = Gummy(center=(400, 100), radius=100, num_points=20, k_perimeter=800, k_center=500, damping=1)

    running = True
    while running:
        dt = clock.tick(FPS) / 1000 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        gummy.update(dt)
        screen.fill((200, 200, 200))
        pygame.draw.rect(screen, (100, 100, 100), (0, GROUND_Y, WIDTH, HEIGHT - GROUND_Y))
        gummy.draw(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
