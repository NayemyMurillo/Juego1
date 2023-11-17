import pygame
import os
import random

pygame.init()
ancho = 800
alto = 600
screen = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("Cat, run!")

# Música de fondo
pygame.mixer.music.load("musica.mpeg")
pygame.mixer.music.play(-1)

# Logo del juego
logo = pygame.image.load("logo.png")
pygame.display.set_icon(logo)

jetpack_image = pygame.image.load(os.path.join("salta.png"))
obstacle_image = pygame.image.load(os.path.join("obs1.png"))
misil_image = pygame.image.load(os.path.join("misil.png"))
background_image = pygame.image.load(os.path.join("fondo1.png"))
game_over_image = pygame.image.load(os.path.join("over.jpg"))
moneda_image = pygame.image.load(os.path.join("moneda.png")).convert_alpha()
sonido_abajo = pygame.image.load(os.path.join("bajar.png"))
sonido_mute = pygame.image.load(os.path.join("apagado.png"))
sonido_subir = pygame.image.load(os.path.join("subir.png"))
monedas = []
obstaculos = []
misiles = []  # Lista de misiles
GENERAR_MONEDAS_EVENTO = pygame.USEREVENT + 1
GENERAR_OBSTACULO_EVENTO = pygame.USEREVENT + 2
GENERAR_MISIL_EVENTO = pygame.USEREVENT + 3  # Nuevo evento para generar misiles

def dibujar_texto (surface, text, size,x,y):
    font= pygame.font.SysFont("serif",size)
    text_surface= font.render(text, True, [255,255,255])
    text_rect= text_surface.get_rect()
    text_rect.midtop=(x,y)
    surface.blit(text_surface,text_rect)

def generar_fila_de_monedas(y):
    fila_de_monedas = []
    for i in range(random.randint(5, 10)):
        x = 800 + i * moneda_image.get_width()  # Coloca las monedas en una fila
        fila_de_monedas.append(pygame.Rect(x, y, moneda_image.get_width(), moneda_image.get_height()))
    return fila_de_monedas

def generar_obstaculo():
    y = random.choice(y_positions)
    x = 800
    return pygame.Rect(x, y, obstacle_image.get_width(), obstacle_image.get_height())

def generar_misil(y):
    x = 800
    return pygame.Rect(x, y, misil_image.get_width(), misil_image.get_height())

pygame.time.set_timer(GENERAR_MONEDAS_EVENTO, random.randint(4000, 8000))
pygame.time.set_timer(GENERAR_OBSTACULO_EVENTO, random.randint(5000, 10000))
pygame.time.set_timer(GENERAR_MISIL_EVENTO, random.randint(10000, 20000))

y_positions = [random.randint(100, 500) for _ in range(10)]

jetpack_x = 50
jetpack_y = 300
jetpack_width = jetpack_image.get_width()
jetpack_height = jetpack_image.get_height()

scaled_image = pygame.transform.scale(background_image, (800, 600))
scaled_image2 = pygame.transform.scale(game_over_image, (800, 600))

clock = pygame.time.Clock()
score = 0
running = True
fondo_x = 0
fondo_velocidad = 8
gravity = 6


def pantalla():
    global fondo_x
    fondo_avanza = fondo_x % background_image.get_rect().width
    screen.blit(background_image, (fondo_avanza - background_image.get_rect().width, 0))
    if fondo_avanza < ancho:
        screen.blit(background_image, (fondo_avanza, 0))
    fondo_x -= fondo_velocidad
    screen.blit(jetpack_image, (jetpack_x, jetpack_y))
    for moneda_rect in monedas:
        screen.blit(moneda_image, moneda_rect)

    # Solo mueve el obstáculo 1 en la primera iteración
    if len(obstaculos) == 0:
        obstaculo_rect = generar_obstaculo()
        obstaculos.append(obstaculo_rect)
    for obstaculo_rect in obstaculos:
        # No muevas los obstáculos aquí
        # Verificar colisiones con los obstáculos
        if (
            jetpack_x < obstaculo_rect.x + obstaculo_rect.width - 10
            and jetpack_x + jetpack_width - 10 > obstaculo_rect.x
            and jetpack_y < obstaculo_rect.y + obstaculo_rect.height - 10
            and jetpack_y + jetpack_height - 10 > obstaculo_rect.y
        ):
            screen.blit(scaled_image2, (0, 0))
            pygame.display.flip()
            pygame.time.delay(3000)
            running = False
        screen.blit(obstacle_image, obstaculo_rect)

    for misil_rect in misiles:
        screen.blit(misil_image, misil_rect)

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == GENERAR_MONEDAS_EVENTO:
            monedas.extend(generar_fila_de_monedas(y_positions[random.randint(0, 9)]))
        elif event.type == GENERAR_OBSTACULO_EVENTO:
            y = random.choice([pos for pos in y_positions if pos not in [moneda_rect.y for moneda_rect in monedas]])
            y = max(100, min(y, 500))  # Asegura que la posición y esté dentro de los límites
            obstaculos.append(generar_obstaculo())
        elif event.type == GENERAR_MISIL_EVENTO:
            y = random.choice([pos for pos in y_positions if pos not in [moneda_rect.y for moneda_rect in monedas]])
            misiles.append(generar_misil(y))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and jetpack_x > 0:
        jetpack_x -= 5
    if keys[pygame.K_RIGHT] and jetpack_x < 700 - jetpack_width:
        jetpack_x += 5
    if keys[pygame.K_UP] and jetpack_y > 0:
        jetpack_y -= 13
    
    # Volumen baja
    if keys[pygame.K_o] and pygame.mixer.music.get_volume() > 0.0:
        pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() - 0.01)
        screen.blit(sonido_abajo, (100, 87))
    elif keys[pygame.K_o] and pygame.mixer.music.get_volume() == 0.0:
        screen.blit(sonido_mute, (100, 87))
    
    # Volumen sube
    if keys[pygame.K_p] and pygame.mixer.music.get_volume() < 1.0:
        pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() + 0.01)
        screen.blit(sonido_subir, (100, 87))
    # Desactivar volumen 
    elif keys[pygame.K_i]:
        pygame.mixer.music.set_volume(0.0)
        screen.blit(sonido_mute, (100, 87))

    if jetpack_y < 600 - jetpack_height:
        jetpack_y += gravity

    screen.blit(scaled_image, (0, 0))

    for moneda_rect in monedas:
        moneda_rect.x -= fondo_velocidad
        screen.blit(moneda_image, moneda_rect)

    for obstaculo_rect in obstaculos:
        obstaculo_rect.x -= fondo_velocidad
        screen.blit(obstacle_image, obstaculo_rect)
 
        # Verificar colisiones con los obstáculos
        if jetpack_x < obstaculo_rect.x + obstaculo_rect.width and jetpack_x + jetpack_width > obstaculo_rect.x and jetpack_y < obstaculo_rect.y + obstaculo_rect.height and jetpack_y + jetpack_height > obstaculo_rect.y:
            screen.blit(scaled_image2, (0, 0))
            pygame.display.flip()
            pygame.time.delay(3000)
            running = False

    for misil_rect in misiles:
        misil_rect.x -= fondo_velocidad + 5  # Ajusta la velocidad de los misiles
        screen.blit(misil_image, misil_rect)

    # Verificar colisiones con las monedas
    for moneda_rect in monedas:
        if jetpack_x < moneda_rect.x < jetpack_x + jetpack_width and jetpack_y < moneda_rect.y < jetpack_y + jetpack_height:
            monedas.remove(moneda_rect)
            score += 1

    # Verificar colisiones con los misiles
    for misil_rect in misiles:
        if jetpack_x < misil_rect.x < jetpack_x + jetpack_width and jetpack_y < misil_rect.y < jetpack_y + jetpack_height:
            screen.blit(scaled_image2, (0, 0))
            pygame.display.flip()
            pygame.time.delay(3000)
            running = False

    # Eliminar misiles que salieron de la pantalla
    misiles = [misil for misil in misiles if misil.x > -misil.width]
    pantalla()
    dibujar_texto(screen, str(score),25 ,70,10)
    pygame.display.flip()

pygame.quit()
