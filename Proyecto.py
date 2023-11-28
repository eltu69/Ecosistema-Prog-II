import pygame
import random
import math
import time

pygame.init()

width = 800
height = 600
screen = pygame.display.set_mode((width, height))

black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
brown = (139, 69, 19)
red = (255, 0, 0)
blue = (0, 0, 255)

font = pygame.font.SysFont("Arial", 20)

clock = pygame.time.Clock()
running = True
fps = 30

# Añadimos una capacidad de carga para las plantas
plant_capacity = 1000

class Plant(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.radius = 5
        self.image = pygame.Surface((self.radius * 2, self.radius * 2))
        self.image.fill(green)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.energy = 10

    def update(self):
        if self.energy <= 0:
            self.kill()
        if self.energy >= 10 and random.random() < 0.02 and len(plants) < plant_capacity:
            self.reproduce()

    def reproduce(self):
        x = self.rect.x + random.randint(-50, 50)
        y = self.rect.y + random.randint(-50, 50)
        x = max(0, min(x, width - self.radius * 2))
        y = max(0, min(y, height - self.radius * 2))
        new_plant = Plant(x, y)
        plants.add(new_plant)
        self.energy /= 2



class Herbivore(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.radius = 5
        self.image = pygame.Surface((self.radius * 2, self.radius * 2))
        self.image.fill(brown)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.energy = 10
        self.speed = 4
        self.direction = random.randint(0, 359)

    def update(self):
        if self.energy <= 0:
            self.kill()
        else:
            self.move()  
            self.eat()
            if self.energy >= 20 and random.random() < 0.02: 
                self.reproduce()

    def move(self):
        closest_plant = min(plants, key=lambda plant: self.distance_to_sprite(plant))
        closest_carnivore = min(carnivores, key=lambda carnivore: self.distance_to_sprite(carnivore))

        if self.distance_to_sprite(closest_carnivore) < 100:  
            self.direction = (self.angle_to_sprite(closest_carnivore) + 180) % 360
        elif self.distance_to_sprite(closest_plant) < 50:  
            self.direction = self.angle_to_sprite(closest_plant)
        else:
            self.direction += random.randint(-10, 10)  

        dx = self.speed * math.cos(math.radians(self.direction))
        dy = self.speed * math.sin(math.radians(self.direction))
        self.rect.x += dx
        self.rect.y += dy
        self.rect.x = max(0, min(self.rect.x, width - self.radius * 2))
        self.rect.y = max(0, min(self.rect.y, height - self.radius * 2))

    def distance_to_sprite(self, sprite):
        dx = sprite.rect.x - self.rect.x
        dy = sprite.rect.y - self.rect.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def angle_to_sprite(self, sprite):
        dx = sprite.rect.x - self.rect.x
        dy = sprite.rect.y - self.rect.y
        return math.degrees(math.atan2(dy, dx))

    def eat(self):
        plant = pygame.sprite.spritecollideany(self, plants)
        if plant:
            self.energy += 5  
            plant.energy -= 5  

    def reproduce(self):
        x = self.rect.x + random.randint(-50, 50)
        y = self.rect.y + random.randint(-50, 50)
        x = max(0, min(x, width - self.radius * 2))
        y = max(0, min(y, height - self.radius * 2))
        new_herbivore = Herbivore(x, y)
        herbivores.add(new_herbivore)
        self.energy /= 2

class Carnivore(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.radius = 11
        self.image = pygame.Surface((self.radius * 2, self.radius * 2))
        self.image.fill(red)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.energy = 200
        self.speed = 4
        self.direction = random.randint(0, 359)

    def update(self):
        if self.energy <= 0:
            self.kill()
        if self.energy >= 100 and random.random() < 0.02:  
            self.reproduce()
        self.move()
        self.eat()
        self.energy -= 1  

    def move(self):
        closest_herbivore = min(herbivores, key=lambda herbivore: self.distance_to_sprite(herbivore))
        if self.distance_to_sprite(closest_herbivore) < 200:  
            self.direction = self.angle_to_sprite(closest_herbivore)
        else:
            self.direction += random.randint(-10, 10)  

        dx = self.speed * math.cos(math.radians(self.direction))
        dy = self.speed * math.sin(math.radians(self.direction))
        self.rect.x += dx
        self.rect.y += dy
        self.rect.x = max(0, min(self.rect.x, width - self.radius * 2))
        self.rect.y = max(0, min(self.rect.y, height - self.radius * 2))

    def distance_to_sprite(self, sprite):
        dx = sprite.rect.x - self.rect.x
        dy = sprite.rect.y - self.rect.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def angle_to_sprite(self, sprite):
        dx = sprite.rect.x - self.rect.x
        dy = sprite.rect.y - self.rect.y
        return math.degrees(math.atan2(dy, dx))

    def eat(self):
        herbivore = pygame.sprite.spritecollideany(self, herbivores)
        if herbivore:
            self.energy += 15  
            herbivore.kill()

    def reproduce(self):
        x = self.rect.x + random.randint(-50, 50)
        y = self.rect.y + random.randint(-50, 50)
        x = max(0, min(x, width - self.radius * 2))
        y = max(0, min(y, height - self.radius * 2))
        new_carnivore = Carnivore(x, y)
        carnivores.add(new_carnivore)
        self.energy /= 2

class Meteorite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.radius = 100  # Radio de impacto del meteorito
        self.image = pygame.Surface((self.radius * 2, self.radius * 2))
        pygame.draw.circle(self.image, blue, (self.radius, self.radius), self.radius)
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (-100, -100)  # Inicialmente fuera de la pantalla

    def strike(self, counter_value, plants, herbivores, carnivores):
        if counter_value > 0 and counter_value % 5 == 0:  # Cambia esto a 100 para que el meteorito golpee cada 100 ciclos
            # Define la zona de impacto del meteorito (x, y)
            x = random.randint(self.radius, width - self.radius)
            y = random.randint(self.radius, height - self.radius)
            self.rect.center = (x, y)
            for group in [plants, herbivores, carnivores]:
                for organism in list(group):
                    if self.in_impact_zone(organism):
                        organism.kill()
        else:
            self.rect.center = (-100, -100)  # Mueve el meteorito fuera de la pantalla

    def in_impact_zone(self, organism):
        distance = math.sqrt((organism.rect.centerx - self.rect.centerx)**2 + (organism.rect.centery - self.rect.centery)**2)
        return distance <= self.radius




plants = pygame.sprite.Group()
herbivores = pygame.sprite.Group()
carnivores = pygame.sprite.Group()

# Función para contar cada 5 segundos
def count_timer():
    start_time = time.time()
    counter = 0
    while True:
        current_time = time.time()
        if current_time - start_time >= 5:
            counter += 1
            start_time = current_time
        yield counter

counter_generator = count_timer()

for i in range(100):
    x = random.randint(0, width - 10)
    y = random.randint(0, height - 10)
    plant = Plant(x, y)
    plants.add(plant)

for i in range(20):
    x = random.randint(0, width - 20)
    y = random.randint(0, height - 20)
    herbivore = Herbivore(x, y)
    herbivores.add(herbivore)

for i in range(10):
    x = random.randint(0, width - 30)
    y = random.randint(0, height - 30)
    carnivore = Carnivore(x, y)
    carnivores.add(carnivore)

meteorites = pygame.sprite.GroupSingle()

meteorite = Meteorite()
meteorites.add(meteorite)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if random.random() < 0.2: 
        x = random.randint(0, width - 10)
        y = random.randint(0, height - 10)
        plant = Plant(x, y)
        plants.add(plant)

    plants.update()
    herbivores.update()
    carnivores.update()
    meteorites.update()
    

    screen.fill(white)
    plants.draw(screen)
    herbivores.draw(screen)
    carnivores.draw(screen)
    meteorites.draw(screen)
    

    counter_value = next(counter_generator)
    meteorite.strike(counter_value, plants, herbivores, carnivores)
    text = font.render(f"Plantas: {len(plants)} Herbívoros: {len(herbivores)} Carnívoros: {len(carnivores)} Ciclos: {counter_value}", True, black)
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()