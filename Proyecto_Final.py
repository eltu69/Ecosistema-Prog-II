import pygame
import random
import math
import time

pygame.init()

# Definición de constantes y configuración inicial de Pygame
width = 1000
height = 800
screen = pygame.display.set_mode((width, height))

# Definición de colores
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
brown = (139, 69, 19)
red = (255, 0, 0)
blue = (0, 0, 255)

# Configuración de fuente
font = pygame.font.SysFont("Arial", 20)

# Configuración de reloj y FPS
clock = pygame.time.Clock()
running = True
fps = 30

# Añadimos una capacidad de carga para las plantas
plant_capacity = 400

# Definición de la clase Plant
class Plant(pygame.sprite.Sprite):
    images = ['planta.png','planta3.png', 'planta4.png', 'planta5.png']  # Lista de imágenes
    
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.radius = 5  # Añade esta línea para definir el atributo radius
        image_path = random.choice(self.images)  # Selecciona una imagen aleatoria de la lista
        self.image = pygame.image.load(image_path)  # Carga la imagen
        self.image = pygame.transform.scale(self.image, (self.radius * 2, self.radius * 2))  # Ajusta el tamaño de la imagen
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.energy = 10

    def update(self):
        # Verifica si la energía es menor o igual a cero y hay más de dos plantas para eliminarla
        if self.energy <= 0 and len(plants) > 2:
            self.kill()
        # Verifica si la energía es mayor o igual a 10 y se cumple una probabilidad para reproducirse
        if self.energy >= 10 and random.random() < 0.02 and len(plants) < plant_capacity:
            self.reproduce()

    def reproduce(self):
    # Genera nuevas plantas cercanas con energía dividida
        x = self.rect.x + random.randint(-50, 50)
        y = self.rect.y + random.randint(-50, 50)
        x = max(0, min(x, width - self.radius * 2))
        y = max(0, min(y, height - self.radius * 2))
        new_plant = Plant(x, y)
        plants.add(new_plant)
        self.energy /= 2

        # Asegura que siempre haya al menos dos plantas
        if len(plants) < 2:
            x = random.randint(0, width - 10)
            y = random.randint(0, height - 10)
            new_plant = Plant(x, y)
            plants.add(new_plant)

# Definición de la clase Herbivore
class Herbivore(pygame.sprite.Sprite):
    images = ['herviboro.png', 'herviboro2.png', 'herviboro3.png' , 'herviboro4.png']  # Lista de imágenes
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.radius = 10  # Añade esta línea para definir el atributo radius
        image_path = random.choice(self.images)  # Selecciona una imagen aleatoria de la lista
        self.image = pygame.image.load(image_path)  # Carga la imagen
        self.image = pygame.transform.scale(self.image, (self.radius * 2, self.radius * 2))  # Ajusta el tamaño de la imagen
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.energy = 10
        self.speed = 4
        self.direction = random.randint(0, 359)

    def update(self):
        # Verifica si la energía es menor o igual a cero y hay más de dos herbívoros para eliminarlo
        if self.energy <= 0 and len(herbivores) > 2:
            self.kill()
        else:
            self.move()
            self.eat()
            # Verifica si la energía es mayor o igual a 20 y se cumple una probabilidad para reproducirse
            if self.energy >= 20 and random.random() < 0.02:
                self.reproduce()

    def move(self):
        # Calcula la dirección para moverse hacia la planta más cercana o aleatoriamente
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
        # Calcula la distancia entre el herbívoro y otro sprite
        dx = sprite.rect.x - self.rect.x
        dy = sprite.rect.y - self.rect.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def angle_to_sprite(self, sprite):
        # Calcula el ángulo entre el herbívoro y otro sprite
        dx = sprite.rect.x - self.rect.x
        dy = sprite.rect.y - self.rect.y
        return math.degrees(math.atan2(dy, dx))

    def eat(self):
        # Realiza la colisión con una planta y aumenta la energía
        plant = pygame.sprite.spritecollideany(self, plants)
        if plant:
            self.energy += 5
            plant.energy -= 5

    def reproduce(self):
    # Genera nuevos herbívoros cercanos con energía dividida
        x = self.rect.x + random.randint(-50, 50)
        y = self.rect.y + random.randint(-50, 50)
        x = max(0, min(x, width - self.radius * 2))
        y = max(0, min(y, height - self.radius * 2))
        new_herbivore = Herbivore(x, y)
        herbivores.add(new_herbivore)
        self.energy /= 2

        # Asegura que siempre haya al menos dos herbívoros
        if len(herbivores) < 2:
            x = random.randint(0, width - 20)
            y = random.randint(0, height - 20)
            new_herbivore = Herbivore(x, y)
            herbivores.add(new_herbivore)

# Definición de la clase Carnivore
class Carnivore(pygame.sprite.Sprite):
    images = ['carnivoro.png','carnivoro2.png','carnivoro3.png','carnivoro4.png']  # Lista de imágenes

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.radius = 15  # Añade esta línea para definir el atributo radius
        image_path = random.choice(self.images)  # Selecciona una imagen aleatoria de la lista
        self.image = pygame.image.load(image_path)  # Carga la imagen
        self.image = pygame.transform.scale(self.image, (self.radius * 2, self.radius * 2))  # Ajusta el tamaño de la imagen
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.energy = 200
        self.speed = 4
        self.direction = random.randint(0, 359)

    def update(self):
        # Verifica si la energía es menor o igual a cero y hay más de dos carnívoros para eliminarlo
        if self.energy <= 0 and len(carnivores) > 2:
            self.kill()
        # Verifica si la energía es mayor o igual a 100 y se cumple una probabilidad para reproducirse
        if self.energy >= 100 and random.random() < 0.02:
            self.reproduce()
        self.move()
        self.eat()
        self.energy -= 1

    def move(self):
        # Calcula la dirección para moverse hacia el herbívoro más cercano o aleatoriamente
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
        # Calcula la distancia entre el carnívoro y otro sprite
        dx = sprite.rect.x - self.rect.x
        dy = sprite.rect.y - self.rect.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def angle_to_sprite(self, sprite):
        # Calcula el ángulo entre el carnívoro y otro sprite
        dx = sprite.rect.x - self.rect.x
        dy = sprite.rect.y - self.rect.y
        return math.degrees(math.atan2(dy, dx))

    def eat(self):
        # Realiza la colisión con un herbívoro y aumenta la energía
        herbivore = pygame.sprite.spritecollideany(self, herbivores)
        if herbivore:
            self.energy += 15
            herbivore.kill()

    def reproduce(self):
        # Genera nuevos carnívoros cercanos con energía dividida
        x = self.rect.x + random.randint(-50, 50)
        y = self.rect.y + random.randint(-50, 50)
        x = max(0, min(x, width - self.radius * 2))
        y = max(0, min(y, height - self.radius * 2))
        new_carnivore = Carnivore(x, y)
        carnivores.add(new_carnivore)
        self.energy /= 2

        # Asegura que siempre haya al menos dos carnívoros
        if len(carnivores) < 2:
            x = random.randint(0, width - 30)
            y = random.randint(0, height - 30)
            new_carnivore = Carnivore(x, y)
            carnivores.add(new_carnivore)

# Definición de la clase Meteorite
class Meteorite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.radius = 100  # Radio de impacto del meteorito
        self.image = pygame.image.load('meteorito.png')  # Carga la imagen
        self.image = pygame.transform.scale(self.image, (self.radius * 2, self.radius * 2))  # Ajusta el tamaño de la imagen
        self.rect = self.image.get_rect()
        self.rect.center = (-100, -100)  # Posición inicial fuera de la pantalla
        self.strike_position = None  # Posición del impacto

    def strike(self, counter_value, plants, herbivores, carnivores):
        # Verifica si el contador es mayor que cero y es un múltiplo de 10 (cambiar a 100 para golpear cada 100 ciclos)
        if counter_value > 0 and counter_value % 10 == 0:
            # Define la zona de impacto del meteorito (x, y)
            x = random.randint(self.radius, width - self.radius)
            y = random.randint(self.radius, height - self.radius)
            self.rect.center = (x, y)
            # Elimina los organismos dentro del área de impacto
            for group in [plants, herbivores, carnivores]:
                for organism in list(group):
                    if self.in_impact_zone(organism.rect.center):
                        organism.kill()

            # Regenera los organismos si su número es menor que 2
            if len(plants) < 2:
                for _ in range(2 - len(plants)):
                    x = random.randint(0, width - 10)
                    y = random.randint(0, height - 10)
                    new_plant = Plant(x, y)
                    plants.add(new_plant)
            if len(herbivores) < 2:
                for _ in range(2 - len(herbivores)):
                    x = random.randint(0, width - 20)
                    y = random.randint(0, height - 20)
                    new_herbivore = Herbivore(x, y)
                    herbivores.add(new_herbivore)
            if len(carnivores) < 2:
                for _ in range(2 - len(carnivores)):
                    x = random.randint(0, width - 30)
                    y = random.randint(0, height - 30)
                    new_carnivore = Carnivore(x, y)
                    carnivores.add(new_carnivore)
        else:
            self.rect.center = (-100, -100)  # Mueve el meteorito fuera de la pantalla

    def in_impact_zone(self, position):
        # Verifica si una posición está dentro del área de impacto del meteorito
        distance = math.sqrt((position[0] - self.rect.centerx)**2 + (position[1] - self.rect.centery)**2)
        return distance <= self.radius


class Fire(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.initial_radius = 10
        self.max_radius = 40
        self.image = pygame.image.load('fire.png')  # Agrega la ruta de la imagen del fuego
        self.image = pygame.transform.scale(self.image, (self.initial_radius * 2, self.initial_radius * 2))  # Ajusta el tamaño de la imagen
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.burning_time = 180  # Duración del incendio en ciclos (3 segundos a 60 FPS)
        self.max_burning_time = self.burning_time

    def update(self):
        if self.burning_time > 0:
            # Ajusta el tamaño del fuego según el tiempo restante
            current_radius = int(self.initial_radius + (self.max_radius - self.initial_radius) *
                                 (1 - self.burning_time / self.max_burning_time))
            self.image = pygame.image.load('fire.png')  # Recarga la imagen del fuego
            self.image = pygame.transform.scale(self.image, (current_radius * 2, current_radius * 2))  # Ajusta el tamaño de la imagen
            self.burning_time -= 1
            # Verifica si hay colisiones con plantas, herbívoros y carnívoros
            for group in [plants, herbivores, carnivores]:
                for organism in pygame.sprite.spritecollide(self, group, False):
                    # Reduce la energía de las plantas y elimina herbívoros y carnívoros
                    if isinstance(organism, Plant):
                        organism.energy -= 2
                    elif isinstance(organism, Herbivore) or isinstance(organism, Carnivore):
                        organism.kill()
        else:
            self.kill()

class Raindrop(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.size = 2
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(blue)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, width)
        self.rect.y = random.randint(0, height)
        self.lifespan = 180  # Duración de la lluvia en ciclos (3 segundos a 60 FPS)

    def update(self, plants):
        # Verificar colisiones con plantas y aumentar su energía
        for plant in pygame.sprite.spritecollide(self, plants, False):
            plant.energy += 5

        # Reducir el temporizador y eliminar la gota de lluvia si ha alcanzado su límite de vida
        self.lifespan -= 1
        if self.lifespan <= 0:
            self.kill()


# Creación de grupos de sprites
plants = pygame.sprite.Group()
herbivores = pygame.sprite.Group()
carnivores = pygame.sprite.Group()
meteorites = pygame.sprite.GroupSingle()
fires = pygame.sprite.Group()
raindrops = pygame.sprite.Group()

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

# Inicialización de organismos
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

# Inicialización del meteorito
meteorite = Meteorite()
meteorites.add(meteorite)

# Bucle principal del juego
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Evento de incendio al presionar la tecla ESPACIO
                x = random.randint(0, width - 30)
                y = random.randint(0, height - 30)
                new_fire = Fire(x, y)
                fires.add(new_fire)
            elif event.key == pygame.K_a:
                # Evento de lluvia al presionar la tecla A
                for _ in range(50):  # Número de gotas de lluvia
                    raindrop = Raindrop()
                    raindrops.add(raindrop)

    # Probabilidad de crear nuevas plantas
    if random.random() < 10:
        x = random.randint(0, width - 10)
        y = random.randint(0, height - 10)
        plant = Plant(x, y)
        plants.add(plant)

    # Actualización de los grupos de sprites
    plants.update()
    herbivores.update()
    carnivores.update()
    meteorites.update()
    fires.update()
    raindrops.update(plants)
    for raindrop in raindrops.sprites():
        if raindrop.lifespan <= 0:
            raindrop.kill()

    screen.fill(white)
    plants.draw(screen)
    herbivores.draw(screen)
    carnivores.draw(screen)
    meteorites.draw(screen)
    fires.draw(screen)
    raindrops.draw(screen)

    counter_value = next(counter_generator)
    meteorite.strike(counter_value, plants, herbivores, carnivores)

    # Renderizar y mostrar los textos
    text_a = font.render('Presiona "A" para hacer llover (Recomendable solo presionar una vez)', True, black)
    text_space = font.render('Presiona "ESPACIO" para hacer un incendio forestal', True, black)
    text_meteorito = font.render('Cada 10 ciclos caera un meteorito', True, black)
    screen.blit(text_a, (10, height - 60))
    screen.blit(text_space, (10, height - 30))
    screen.blit(text_meteorito, (10, height - 90))

    # Renderizar y mostrar estadísticas
    text_stats = font.render(f"Plantas: {len(plants)} Herbívoros: {len(herbivores)} Carnívoros: {len(carnivores)} Ciclos: {counter_value}", True, black)
    screen.blit(text_stats, (10, 10))

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()