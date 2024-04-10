import numpy as np
from EnigmaPython.EnigmaPython import EnigmaPython
import pygame
import sys

# Initialiser Pygame
pygame.init()

# Définir les couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# Définir les dimensions de la fenêtre
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Définir les dimensions et la disposition des touches du clavier
KEY_WIDTH = 50
KEY_HEIGHT = 50
KEY_MARGIN = 10

# Liste des touches du clavier (QWERTZ)
keys = [
    'qwertzuiop',
    'asdfghjkl',
    'yxcvbnm'
]

# Calculer les marges horizontales et verticales pour centrer les touches dans la fenêtre
HORIZONTAL_MARGIN = (WINDOW_WIDTH - (len(keys[0]) * (KEY_WIDTH + KEY_MARGIN))) // 2
VERTICAL_MARGIN = (WINDOW_HEIGHT - (len(keys) * (KEY_HEIGHT + KEY_MARGIN))) // 2

# Créer une fenêtre
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('EnigmaPython')

# Fonction pour obtenir les coordonnées de la touche correspondant à la lettre
def get_key_coordinates(letter):
    for row in range(len(keys)):
        for col in range(len(keys[row])):
            if keys[row][col] == letter:
                return (col, row)
    return None

# Garder une trace de l'état des touches du clavier
keys_pressed = set()

# Créer une instance de l'objet EnigmaPython
Enigma = EnigmaPython()

# Déclarer une variable pour stocker la touche mise en surbrillance
highlighted_key = None

# Définir les dimensions de la zone de texte
TEXT_WIDTH = WINDOW_WIDTH
TEXT_HEIGHT = 50

# Définir la police et la taille de la police pour le texte
font = pygame.font.Font(None, 36)

letters = ''

# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Vérifier si la touche appuyée est une lettre du clavier
            if event.key >= pygame.K_a and event.key <= pygame.K_z:
                letter = chr(event.key)
                letters += letter
                # Utiliser la fonction inputOutput pour obtenir la touche à mettre en surbrillance
                letter_to_highlight = Enigma.inputOutput(letter)
                if letter_to_highlight:
                    keys_pressed.add(letter_to_highlight)  # Ajouter la touche à l'ensemble des touches enfoncées
                    highlighted_key = letter  # Mémoriser la touche mise en surbrillance
        elif event.type == pygame.KEYUP:
            # Si la touche relâchée correspond à la touche mise en surbrillance
            if event.key >= pygame.K_a and event.key <= pygame.K_z:
                letter = chr(event.key)
                if highlighted_key is not None and letter == highlighted_key:
                    keys_pressed = set()  # Retirer la touche de l'ensemble des touches enfoncées
                    highlighted_key = None  # Réinitialiser la touche mise en surbrillance
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            # Vérifiez si le clic de souris se produit à l'intérieur de la zone de texte
            if text_rect.collidepoint(mouse_pos):
                editing_mode = True
            else:
                editing_mode = False

    # Effacer l'écran
    window.fill(WHITE)

    text_surface_top = font.render('Encrypted message :', True, BLACK)
    text_rect_top = text_surface_top.get_rect(center=(WINDOW_WIDTH // 2, TEXT_HEIGHT))
    window.blit(text_surface_top, text_rect_top)

    # Dessiner la zone de texte au-dessus du clavier
    text_surface_top = font.render(Enigma.getEcryptLetters(), True, BLACK)
    text_rect_top = text_surface_top.get_rect(center=(WINDOW_WIDTH // 2, TEXT_HEIGHT * 2))
    window.blit(text_surface_top, text_rect_top)

    # Dessiner la zone de texte en dessous du clavier
    text_surface_bottom = font.render(letters, True, BLACK)
    text_rect_bottom = text_surface_bottom.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - TEXT_HEIGHT // 2))
    window.blit(text_surface_bottom, text_rect_bottom)

    text_surface_bottom = font.render('Rotors Config :', True, BLACK)
    text_rect_bottom = text_surface_bottom.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - (TEXT_HEIGHT*4.5) // 2))
    window.blit(text_surface_bottom, text_rect_bottom)

    text_surface_bottom = font.render(Enigma.getConfig(), True, BLACK)
    text_rect_bottom = text_surface_bottom.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - (TEXT_HEIGHT*3) // 2))
    window.blit(text_surface_bottom, text_rect_bottom)

    # Dessiner les touches du clavier
    for row in range(len(keys)):
        for col in range(len(keys[row])):
            key = keys[row][col]
            rect = pygame.Rect(
                HORIZONTAL_MARGIN + col * (KEY_WIDTH + KEY_MARGIN),
                VERTICAL_MARGIN + row * (KEY_HEIGHT + KEY_MARGIN),
                KEY_WIDTH,
                KEY_HEIGHT
            )
            pygame.draw.rect(window, BLACK, rect, 1)
            font = pygame.font.Font(None, 36)
            text_surface = font.render(key, True, BLACK)
            text_rect = text_surface.get_rect(center=rect.center)
            window.blit(text_surface, text_rect)

            # Dessiner la surbrillance si la touche est enfoncée
            if key in keys_pressed:
                pygame.draw.rect(window, YELLOW, rect, 3)  # Augmenter l'épaisseur de la bordure

    # Mettre à jour l'écran
    pygame.display.flip()

# Quitter Pygame
pygame.quit()
sys.exit()
