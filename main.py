import pygame
import random

# Inicialización de Pygame
pygame.init()

# Dimensiones de la ventana del juego
WIDTH, HEIGHT = 900, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Clue Pygame")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Definición de habitaciones y posiciones
rooms = {
    'Cocina': (1, 1),
    'Salón': (2, 1),
    'Comedor': (3, 1),
    'Biblioteca': (1, 2),
    'Sala de Billar': (2, 2),
    'Conservatorio': (3, 2)
}

# Dimensiones de las casillas
CELL_SIZE = 120  # Tamaño de las celdas aumentada

# Jugadores
players = [
    {'name': 'Miss Scarlet', 'color': RED, 'pos': [1, 1], 'cards': [], 'accusation': None},
    {'name': 'Mr. Green', 'color': GREEN, 'pos': [1, 2], 'cards': [], 'accusation': None}
]

# Asesino, Arma, y Habitación aleatorios
murderer = None
weapon = None
crime_room = None

# Variables del juego
current_player = 0
dice_value = 0
game_over = False
message = ""
in_menu = True
dice_rolled = False  # Variable para controlar si el dado ha sido lanzado

# Reglas del Juego
rules = [
    "Reglas:",
    "1. Tira el dado para mover.",
    "2. Sugiere: Asesino, Arma, Habitación.",
    "3. Acusa para ganar."
]

# Instrucciones de control
controls = [
    "Controles:",
    "ESPACIO - Lanzar Dado",
    "ENTER - Hacer Sugerencia",
    "ESC - Volver al Menú"
]


def roll_dice():
    return random.randint(1, 6)


def start_game():
    global murderer, weapon, crime_room, current_player, game_over, message, players
    murderer = random.choice([player['name'] for player in players])
    weapons = ['Candelabro', 'Pistola', 'Cuchillo']
    weapon = random.choice(weapons)
    crime_room = random.choice(list(rooms.keys()))
    current_player = 0
    game_over = False
    message = ""
    global dice_rolled
    dice_rolled = False  # Reiniciar la variable al comenzar el juego


def draw_board():
    win.fill(WHITE)

    # Dibujar habitaciones en la posición actualizada
    for room, (x, y) in rooms.items():
        rect = pygame.Rect(x * CELL_SIZE + 50, y * CELL_SIZE + 70, CELL_SIZE, CELL_SIZE)  # Bajar el tablero
        pygame.draw.rect(win, BLACK, rect, 2)
        font = pygame.font.SysFont(None, 24)
        text = font.render(room, True, BLACK)
        win.blit(text, (rect.x + 10, rect.y + 10))

    # Dibujar jugadores
    for player in players:
        pygame.draw.circle(win, player['color'], (player['pos'][0] * CELL_SIZE + CELL_SIZE // 2 + 50,
                                                  player['pos'][1] * CELL_SIZE + CELL_SIZE // 2 + 70), 20)

    # Mostrar turnos y resultados
    font = pygame.font.SysFont(None, 36)
    turn_text = font.render(f"Turno de: {players[current_player]['name']}", True, BLACK)
    win.blit(turn_text, (10, HEIGHT - 40))

    # Mostrar mensajes
    message_text = font.render(message, True, BLACK)
    message_rect = message_text.get_rect(center=(WIDTH // 2, HEIGHT - 80))
    win.blit(message_text, message_rect)

    # Mostrar reglas
    for i, rule in enumerate(rules):
        rule_text = font.render(rule, True, BLACK)
        win.blit(rule_text, (10, 10 + i * 20))  # Reducir el espacio entre reglas

    # Mostrar controles
    for i, control in enumerate(controls):
        control_text = font.render(control, True, BLACK)
        win.blit(control_text, (WIDTH - 330, 10 + i * 20))  # Lado derecho

    if game_over:
        result_text = font.render(f"{players[current_player]['name']} ha ganado!", True, BLACK)
        win.blit(result_text, (WIDTH // 2 - 100, HEIGHT // 2))

    pygame.display.update()


def make_suggestion(player):
    suggestion = {
        'murderer': random.choice([p['name'] for p in players]),
        'weapon': random.choice(['Candelabro', 'Pistola', 'Cuchillo']),
        'room': list(rooms.keys())[random.randint(0, len(rooms) - 1)]
    }
    return suggestion


def check_suggestion(player_suggestion):
    return (player_suggestion['murderer'] == murderer and
            player_suggestion['weapon'] == weapon and
            player_suggestion['room'] == crime_room)


def move_player(player, steps):
    # Movimiento simple dentro de la cuadrícula
    for _ in range(steps):
        # Intentar mover a la derecha primero
        if player['pos'][0] < 3:  # Mover a la derecha si es posible
            player['pos'][0] += 1
        # Si ya no se puede mover a la derecha, intentar mover hacia abajo
        elif player['pos'][1] < 2:  # Mover hacia abajo si es posible
            player['pos'][1] += 1
        # Si no se puede mover, detenerse
        else:
            break


def draw_menu():
    win.fill(WHITE)
    font = pygame.font.SysFont(None, 48)
    title_text = font.render("Menú Principal", True, BLACK)
    start_text = font.render("Presiona ENTER para comenzar", True, BLACK)
    exit_text = font.render("Presiona ESC para salir", True, BLACK)

    win.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 100))
    win.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2))
    win.blit(exit_text, (WIDTH // 2 - exit_text.get_width() // 2, HEIGHT // 2 + 50))

    pygame.display.update()


# Main loop
running = True
start_game()  # Llamada inicial para preparar el juego
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if in_menu:
        draw_menu()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:  # Comenzar el juego
            in_menu = False
            start_game()
        if keys[pygame.K_ESCAPE]:  # Salir del juego
            running = False

    else:
        draw_board()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not dice_rolled:  # Presiona SPACE para lanzar el dado
            dice_value = roll_dice()  # Lanzar el dado una sola vez
            move_player(players[current_player], dice_value)  # Mover al jugador según el resultado
            message = f"{players[current_player]['name']} lanza el dado y obtiene: {dice_value}"
            dice_rolled = True  # Marcar que el dado ha sido lanzado

        if keys[pygame.K_RETURN] and dice_rolled:  # Presiona ENTER para hacer sugerencia
            suggestion = make_suggestion(players[current_player])
            message = f"{players[current_player]['name']} sugiere: {suggestion['murderer']} con {suggestion['weapon']} en {suggestion['room']}"
            if check_suggestion(suggestion):
                message = f"{players[current_player]['name']} ha ganado el juego!"
                game_over = True
                pygame.display.update()
                pygame.time.delay(3000)  # Esperar 3 segundos antes de regresar al menú
                in_menu = True  # Regresar al menú
            else:
                # Cambiar de turno al final de la sugerencia
                current_player = (current_player + 1) % len(players)
                dice_rolled = False  # Reiniciar el lanzamiento del dado para el siguiente jugador

        if keys[pygame.K_ESCAPE]:  # Volver al menú
            in_menu = True

    pygame.time.delay(100)

pygame.quit()
