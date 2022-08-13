
import pygame
import win32api
import win32con
import win32gui
from tkinter import *
import tkinter as tk

pygame.init()

# Initialize start loop condition
done = False
# Setup window screen
screen_size = pygame.display.Info()
screen = pygame.display.set_mode((screen_size.current_w,screen_size.current_h), pygame.NOFRAME) # Remove window top border
transparency = (255, 0, 128)  # Transparency color
hwnd = pygame.display.get_wm_info()["window"]
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                       win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
# Set window transparency color
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*transparency), 0, win32con.LWA_COLORKEY)

win32gui.SetWindowPos(hwnd, -1, 0, 0, 0, 0, 1)


# Initialize internal clock
clock = pygame.time.Clock()


# Main game loop
while not done:
    # Events loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Quit upon click close button
            done = True
 

    screen.fill(transparency) # Transparent background
    # --- Game logic should go here
    pygame.draw.rect(screen, "red", [300, 300, 300, 300])

    # --- Drawing code should go here
 
    # Updates screen
    pygame.display.flip()
 
    # Determine FPS
    clock.tick(60)