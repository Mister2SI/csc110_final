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

# TODO: why still only 8 samples at once?
pygame.mixer.init(channels=32) # Init with 32 channels, this SHOULD allow 16 stereo samples to play at once

# Program configuration
BTN_W, BTN_H = 200, 100
BTN_MARGIN = 10
WINDOW_WIDTH = BTN_W*5 + BTN_MARGIN*6
WINDOW_HEIGHT = BTN_H*3 + BTN_MARGIN*4
BG = (30, 30, 30)

# Create the screen
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Guitar Chord Soundboard")

# Setup the default tone setting
# 0: ac6
# 1: ac12
# 2: el_st
tone = 0
tone_paths = ["samples/acoustic_6", "samples/acoustic_12", "samples/electric_strat"]

# Whether to sustain or stop sounds on keyup
sustain = False

# Button class
button_font = pygame.font.SysFont(None, 28)
class Button:
    def __init__(self, x, y, w, h, keyname, label, sound):
        self.rect = pygame.Rect(x, y, w, h)
        self.keyname = keyname
        self.label = label
        self.sound = sound
        self.pressed = False
        self.color_normal = (60, 60, 60)
        self.color_pressed = (0, 180, 0)

    def press(self):
        self.pressed = True
        self.sound.play()

    def release(self):
        self.pressed = False
        if not sustain: self.sound.stop()

    def draw(self, surface):
        # Draw the colored rectangle
        color = self.color_pressed if self.pressed else self.color_normal
        pygame.draw.rect(surface, color, self.rect, border_radius=10)

        # Draw label text
        text = button_font.render(self.label, True, (255, 255, 255))   # Get a pygame Surface
        # Get the Surface's rect and position it in the center of the related button
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)       # Draw

# Add keys to bind the buttons to
button_keys = ["q", "w", "e", "r", "t"]

# Function to load the sounds from samples/ and create their buttons
def load_buttons():
    buttons = []    # Create buttons
    # Search samples/ and filter out only the .wav files
    files = [f for f in os.listdir(tone_paths[tone]) if f.lower().endswith(".wav")]

    # Go through each file and create its button
    for idx, filename in enumerate(sorted(files)):
        label = os.path.splitext(filename)[0]       # Remove the file extension
        path = os.path.join(tone_paths[tone], filename)  # Get the path of the sample sound
        sound = pygame.mixer.Sound(path)            # Create the Sound object

        # Grid layout: 5 per row
        col = idx % 5
        row = (idx // 5) + 1    # Skip a row to allow for tone chooser
        x = BTN_MARGIN + col * (BTN_W + BTN_MARGIN)
        y = BTN_MARGIN + row * (BTN_H + BTN_MARGIN)

        # Create the button
        btn = Button(x, y, BTN_W, BTN_H, button_keys[idx], label, sound)
        buttons.append(btn)

    return buttons

# Function to draw labels
subtitle_font = pygame.font.SysFont(None, 24)
title_font = pygame.font.SysFont(None, 36)
def draw_labels(surface):
    # "Tone" label
    tone_title_text = subtitle_font.render("Tone - Cycle with backspace", True, (200, 200, 200))
    tone_title_rect = tone_title_text.get_rect(center=(WINDOW_WIDTH/2, 30))
    surface.blit(tone_title_text, tone_title_rect)

    # The actual selected tone
    tone_name = ""
    match tone:
        case 0:
            tone_name = "1. Acoustic 6-String"
        case 1:
            tone_name = "2. Acoustic 12-String"
        case 2:
            tone_name = "3. Fender Stratocaster"
        case _:
            tone_name = "undefined"

    tone_text = title_font.render(tone_name, True, (255, 255, 255))
    tone_rect = tone_text.get_rect(center=(WINDOW_WIDTH/2, 70))
    surface.blit(tone_text, tone_rect)
    

buttons = load_buttons()
draw_labels(screen)
running = True
while running:
    # Get the EventList
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                running = False

            case pygame.KEYDOWN:
                keyname = pygame.key.name(event.key)
                # Exit on pressing <Esc>
                if event.key == pygame.K_ESCAPE:
                    running = False
                # Cycle tone on backspace
                if event.key == pygame.K_BACKSPACE:
                    if tone == 2: tone = 0
                    else: tone += 1
                    buttons = load_buttons()
                # Sustain on on pressing space
                if event.key == pygame.K_SPACE:
                    sustain = True
                # Activate a button if the pressed key is its assigned value
                for b in buttons:
                    if b.keyname == keyname:
                        b.press()

            case pygame.KEYUP:
                keyname = pygame.key.name(event.key)
                if event.key == pygame.K_SPACE:
                    sustain = False
                # Unpress buttons if their assigned key is released
                for b in buttons:
                    if b.keyname == keyname:
                        b.release()

    # Drawing
    screen.fill((20, 20, 20))
    for b in buttons:
        b.draw(screen)
    draw_labels(screen)

    pygame.display.flip()

pygame.quit()

