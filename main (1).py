import pygame
import os
import random

pygame.init()
ancho = 800
alto = 600
screen = pygame.display.set_mode((ancho, alto))

pygame.display.set_caption("Cat, run!")

# Logo del juego
logo = pygame.image.load("logo.png")
pygame.display.set_icon(logo)

jetpack_image = pygame.image.load(os.path.join("salta.png"))
obstacle_image = pygame.image.load(os.path.join("obs1.png"))
misil_image = pygame.image.load(os.path.join('misil.png'))
background_image = pygame.image.load(os.path.join("fondo1.png"))
game_over_image = pygame.image.load(os.path.join('1258544.jpg'))
moneda_image = pygame.image.load(os.path.join("moneda.png")).convert_alpha()

monedas = []
obstaculos = []
misiles = []  # Lista de misiles
GENERAR_MONEDAS_EVENTO = pygame.USEREVENT + 1
GENERAR_OBSTACULO_EVENTO = pygame.USEREVENT + 2
GENERAR_MISIL_EVENTO = pygame.USEREVENT + 3  # Nuevo evento para generar misiles

def generar_fila_de_monedas(y):
    fila_de_monedas = []
    for i in range(random.randint(5, 10)):
        x = 800 + i * moneda_image.get_width()  # Coloca las monedas en una fila
        fila_de_monedas.append(pygame.Rect(x, y, moneda_image.get_width(), moneda_image.get_height()))
    return fila_de_monedas

def generar_obstaculo(y):
    x = 800
    return pygame.Rect(x, y, obstacle_image.get_width(), obstacle_image.get_height())

def generar_misil(y):
    x = 800
    return pygame.Rect(x, y, misil_image.get_width(), misil_image.get_height())

pygame.time.set_timer(GENERAR_MONEDAS_EVENTO, random.randint(4000, 8000))
pygame.time.set_timer(GENERAR_OBSTACULO_EVENTO, random.randint(8000, 15000))
pygame.time.set_timer(GENERAR_MISIL_EVENTO, random.randint(10000, 20000))

y_positions = [random.randint(100, 500) for _ in range(5)]

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
    for obstaculo_rect in obstaculos:
        screen.blit(obstacle_image, obstaculo_rect)
    for misil_rect in misiles:
        screen.blit(misil_image, misil_rect)

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == GENERAR_MONEDAS_EVENTO:
            monedas.extend(generar_fila_de_monedas(y_positions[random.randint(0, 4)]))
        elif event.type == GENERAR_OBSTACULO_EVENTO:
            y = random.choice([pos for pos in y_positions if pos not in [moneda_rect.y for moneda_rect in monedas]])
            obstaculos.append(generar_obstaculo(y))
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

    if jetpack_y < 600 - jetpack_height:
        jetpack_y += gravity

    screen.blit(scaled_image, (0, 0))

    for moneda_rect in monedas:
        moneda_rect.x -= fondo_velocidad
        screen.blit(moneda_image, moneda_rect)

    for obstaculo_rect in obstaculos:
        obstaculo_rect.x -= fondo_velocidad
        screen.blit(obstacle_image, obstaculo_rect)

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
    pygame.display.flip()

pygame.quit()
