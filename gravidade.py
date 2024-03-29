import pygame
import math
import random

# Inicialização do Pygame
pygame.init()

# Configurações da janela
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Simulação Gravitacional")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Configurações da simulação
G = 20  # Constante gravitacional
dt = 0.1  # Intervalo de tempo

# Classe para representar um objeto massivo
class MassiveObject:
    def __init__(self, x, y, mass, color):
        self.x = x
        self.y = y
        self.mass = mass
        self.color = color
        self.radius = int(math.sqrt(self.mass) / 5)  # Raio diminuído em 5 vezes
        self.velocity_x = 0
        self.velocity_y = 0

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

# Classe para representar uma partícula
class Particle:
    def __init__(self, x, y, mass, velocity_x, velocity_y, color):
        self.x = x
        self.y = y
        self.mass = mass
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.color = color
        self.radius = 2
        self.trail = []

    def update(self, massive_objects, particles):
        force_x = 0
        force_y = 0

        for obj in massive_objects:
            dx = obj.x - self.x
            dy = obj.y - self.y
            distance = math.sqrt(dx**2 + dy**2)

            if distance > self.radius + obj.radius:
                force = G * obj.mass / (distance**2)
                force_x += force * dx / distance
                force_y += force * dy / distance

        for particle in particles:
            if particle != self:
                dx = particle.x - self.x
                dy = particle.y - self.y
                distance = math.sqrt(dx**2 + dy**2)

                if distance > self.radius + particle.radius:
                    force = G * particle.mass / (distance**2)
                    force_x += force * dx / distance
                    force_y += force * dy / distance

        acceleration_x = force_x / self.mass
        acceleration_y = force_y / self.mass

        self.velocity_x += acceleration_x * dt
        self.velocity_y += acceleration_y * dt

        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt

        self.trail.append((int(self.x), int(self.y)))

        self.check_collision(particles)
        self.check_collision_massive(massive_objects)

    def check_collision(self, particles):
        for particle in particles:
            if self == particle:
                continue
            dx = self.x - particle.x
            dy = self.y - particle.y
            distance = math.sqrt(dx**2 + dy**2)
            if distance < self.radius + particle.radius:
                self.resolve_collision(particle)

    def check_collision_massive(self, massive_objects):
        for obj in massive_objects:
            dx = self.x - obj.x
            dy = self.y - obj.y
            distance = math.sqrt(dx**2 + dy**2)
            if distance < self.radius + obj.radius:
                self.resolve_collision_massive(obj)

    def resolve_collision(self, particle):
        # Calculate the vector between the particles
        dx = particle.x - self.x
        dy = particle.y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        
        # Normalize the vector
        nx = dx / distance
        ny = dy / distance
        
        # Calculate the relative velocity
        dvx = particle.velocity_x - self.velocity_x
        dvy = particle.velocity_y - self.velocity_y
        
        # Calculate the velocity along the normal
        vn = dvx * nx + dvy * ny
        
        # No collision if velocities are separating
        if vn > 0:
            return
        
        # Calculate restitution coefficient
        restitution = 1  # for perfectly elastic collision
        
        # Calculate impulse scalar
        impulse = -(1 + restitution) * vn
        impulse /= 1 / self.mass + 1 / particle.mass
        
        # Apply impulse to the particles
        self.velocity_x -= impulse * nx / self.mass
        self.velocity_y -= impulse * ny / self.mass
        
        particle.velocity_x += impulse * nx / particle.mass
        particle.velocity_y += impulse * ny / particle.mass

    def resolve_collision_massive(self, obj):
        # Similar collision handling as resolve_collision, but considering the massive object as immovable
        dx = obj.x - self.x
        dy = obj.y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        
        nx = dx / distance
        ny = dy / distance
        
        dvx = -self.velocity_x
        dvy = -self.velocity_y
        
        vn = dvx * nx + dvy * ny
        
        if vn > 0:
            return
        
        restitution = 1
        
        impulse = -(1 + restitution) * vn
        impulse /= 1 / self.mass  # Massive object considered to have infinite mass
        
        self.velocity_x -= impulse * nx / self.mass
        self.velocity_y -= impulse * ny / self.mass

    def draw(self, screen, show_trails):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

        if show_trails:
            for i in range(len(self.trail) - 1):
                pygame.draw.line(screen, self.color, self.trail[i], self.trail[i + 1])

# Criação dos objetos massivos
central_mass = MassiveObject(width // 2, height // 2, 10000, RED)
massive_objects = [central_mass]

# Criação das partículas
particles = []
num_particles = 80
initial_velocity = 5

for i in range(num_particles):
    x = width // 2
    y = height // 2 - 50 - i * 5
    mass = 10
    velocity_x = initial_velocity
    velocity_y = random.uniform(-0.5, 0.5)  # Pequena variação na velocidade y
    color = (random.randrange(256), random.randrange(256), random.randrange(256))
    particle = Particle(x, y, mass, velocity_x, velocity_y, color)
    particles.append(particle)

# Loop principal
running = True
show_trails = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                show_trails = not show_trails

    screen.fill(BLACK)

    for obj in massive_objects:
        obj.draw(screen)

    for particle in particles:
        particle.update(massive_objects, particles)
        particle.draw(screen, show_trails)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()