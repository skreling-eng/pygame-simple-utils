

import os
import sys
import pygame
from simple_utils import generate_menu, enter_text
import time
import traceback

SCREEN_SIZE = (1280, 820)  # Standard visual novel resolution
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()

bg = "bg.png"

def redraw():
    screen.fill((0,0,0))
    image = pygame.image.load(bg)
    screen.blit(image, (0, 0))

def menu(menu_items):
    menu_sys = ["Add Item", "Exit"]

    textbox_params = (screen, redraw, 200, 200, 500, 500, )
    try:
        selected = generate_menu(*textbox_params, menu_items + menu_sys, line_height=35, font_size=30)
        print(f"selected: {selected}\n")
        if selected in menu_items:
            ii = 0
            while selected != menu_items[ii] and ii<len(menu_items)-1:
                ii+=1
            menu_items[ii] = enter_text(*textbox_params, menu_items[ii])
        elif selected == "Add Item":
            menu_items.append( enter_text(*textbox_params, "New Item") )
        elif selected == "Exit":
            env.exit()
    except Exception as e:
        print(traceback.format_exc())
        env.exit()


def game_start():
    menu_items = ["Text 1", "Text 2"]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        menu(menu_items)
        clock.tick(30)
        pygame.display.flip()

game_start()

