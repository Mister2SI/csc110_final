# CSC 110  |  Fall 2025
# Final
# Jonah Lotegeluaki
# Evan Laatsch
# Fred Panno

# This program reads the samples in a folder and uses the pygame library to
# create buttons for each file that can play on a keypress.

import pygame
import os

pygame.init()
pygame.mixer.init()

SAMPLES_DIR = "samples"
BTN_W, BTN_H = 300, 100
BTN_MARGIN = 10
WINDOW_WIDTH = BTN_W*4 + BTN_MARGIN*5
WINDOW_HEIGHT = 600
BG = (30, 30, 30)

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Soundboard")
font = pygame.font.SysFont(None, 28)

# Button class
class Button:
    def __init__(self, x, y, w, h, keyname, label, sound):
        self.rect = pygame.Rect(x, y, w, h)
        self.keyname = keyname
        self.label = label
        self.sound = sound
        self.pressed = False
        self.color_normal = (60, 60, 60)
        self.color_pressed = (0, 180, 0)

    def draw(self, surface):
        # Draw the colored rectangle
        color = self.color_pressed if self.pressed else self.color_normal
        pygame.draw.rect(surface, color, self.rect, border_radius=10)

        # Draw label text
        text = font.render(self.label, True, (255, 255, 255))
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)

def load_buttons():
    # Create buttons
    buttons = []
    # Search samples/ and filter out only the .wav files
    files = [f for f in os.listdir(SAMPLES_DIR) if f.lower().endswith(".wav")]

    for idx, filename in enumerate(sorted(files)):
        label = os.path.splitext(filename)[0]
        path = os.path.join(SAMPLES_DIR, filename)
        sound = pygame.mixer.Sound(path)

        # Grid layout: 4 per row
        col = idx % 4
        row = idx // 4
        x = BTN_MARGIN + col * (BTN_W + BTN_MARGIN)
        y = BTN_MARGIN + row * (BTN_H + BTN_MARGIN)

        btn = Button(x, y, BTN_W, BTN_H, None, label, sound)
        buttons.append(btn)


    print(files)
    return buttons

buttons = load_buttons()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # Exit on pressing <Esc>
            if event.key == pygame.K_ESCAPE:
                running = False
            # Reload buttons upon pressing backspace
            if event.key == pygame.K_BACKSPACE:
                buttons = load_buttons()
            # Activate a button if the pressed key is its assigned value
            keyname = pygame.key.name(event.key)
            for b in buttons:
                if b.keyname == keyname:
                    b.pressed = True

        if event.type == pygame.KEYUP:
            keyname = pygame.key.name(event.key)
            for b in buttons:
                if b.keyname == keyname:
                    b.pressed = False

    # Drawing
    screen.fill((20, 20, 20))
    for b in buttons:
        b.draw(screen)

    pygame.display.flip()

pygame.quit()

