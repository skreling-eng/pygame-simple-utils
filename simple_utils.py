
import pygame
import os
import sys
import logging
import time
import re
import pygame.scrap as scrap
import traceback

pygame.init()
clock = pygame.time.Clock()


font_path = os.path.join("font", "Courier Prime.ttf")
base_font = pygame.font.Font(font_path, 20)

menu_font_path = os.path.join("font", "Courier Prime Bold.ttf")

class Menu:
    hovered = False
    
    def __init__(self, text, pos, font):
        self.text = text
        self.pos  = pos   
        self.font = font
        self.set_rect()
        self.set_rend()
        self.use_bg = True
    
    def draw(self, surface):
        if self.hovered:
            bg_color = (35, 35, 255)
            color = (255, 255, 255)
        else:
            color = (65, 105, 255)
            bg_color = (255, 255, 255)
        for i in range(-1, 2):
            rend = self.font.render(self.text, True, bg_color)
            rect = rend.get_rect()
            rect.topleft = ( self.pos[0]+i, self.pos[1] )
            surface.blit(rend, rect)
            rect.topleft = ( self.pos[0], self.pos[1]+i )
            surface.blit(rend, rect)
            rect.topleft = ( self.pos[0]+i, self.pos[1]+i )
            surface.blit(rend, rect)
        rend = self.font.render(self.text, True, color)
        rect = rend.get_rect()
        rect.topleft = ( self.pos[0], self.pos[1] )
        surface.blit(rend, rect)

    def set_rend(self):
        self.rend = self.font.render(self.text, True, self.get_color())
        
    def get_color(self):
        return (255, 255, 255) if self.hovered else (65, 105, 255)
            
    def set_rect(self):
        self.set_rend()
        self.rect = self.rend.get_rect()
        self.rect.topleft = self.pos

def generate_menu(screen, redraw, x1, y1, x2, y2, menu_items, line_height=20, col_width=300, font_size=25):

    try:
        menus = []
        def_y_pos = y1 + 5

        max_lines = int((y2 - y1) / line_height)
      
        base_menu_font = pygame.font.Font(font_path, font_size)

        i = 0
        y_pos = def_y_pos
        for item in menu_items:
            if i % max_lines == 0:
                y_pos = def_y_pos
            menus.append(Menu(item, (x1 + int(i / max_lines)*col_width, y_pos), base_menu_font))
            y_pos += line_height
            i+=1
            
            
        pygame.key.set_repeat(3000, 1000)
        running = True
        
        while running:
            redraw()
                
            pygame.event.pump()
            
            for menu in menus:
                if menu.rect.collidepoint(pygame.mouse.get_pos()):
                    menu.hovered = True
                else:
                    menu.hovered = False
                menu.draw(screen)
                
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                    return None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Check for clicked menu item
                    for menu in menus:
                        if menu.hovered:
                            return menu.text
                            
            pygame.time.Clock().tick(30)  # Cap framerate
            
    except Exception as e:
        print(traceback.format_exc())
        return None

def enter_text(screen, redraw, x1, y1, x2, y2, user_text=''):

    scrap.init()
    scrap.set_mode(pygame.SCRAP_CLIPBOARD)

    font_path = os.path.join("font", "Courier Prime.ttf")
    base_font = pygame.font.Font(font_path, 20)
    color_passive = pygame.Color('chartreuse4')
    color = color_passive
    color_active = pygame.Color('lightskyblue3')

    good_chars = "-a-zA-Z0-9'()<>;:_\\.,?! @#$%&*~+={}\\[\\]\""

    font_width = 12
    font_height = 20

    old_style_cursor = False

    if user_text is None:
        user_text = ''

    active = True

    input_rect = pygame.Rect(x1, y1+5, 140, 32)

    pygame.key.set_repeat(300, 50)

    cur_smb = "\u007C"
    cur_pos = len(user_text)

    max_smbs = int((x2 - x1 - 10) / font_width )
    max_lines = int((y2 - y1- 10) / font_height)

    window_start = 0

    selection_active = False
    selection_beg = -1
    selection_end = -1

    (selection_active, selection_beg, selection_end) = (False, -1, -1)

    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False
        
            if event.type == pygame.KEYDOWN:

                mods = pygame.key.get_mods()

                if event.key == pygame.K_BACKSPACE:
                    if selection_active:
                        user_text = user_text[:selection_beg] + user_text[selection_end:]
                        cur_pos = selection_beg
                        (selection_active, selection_beg, selection_end) = (False, -1, -1)
                    elif cur_pos > 0:
                        user_text = user_text[:cur_pos-1] + user_text[cur_pos:]
                        cur_pos -= 1
                elif event.key == pygame.K_DELETE:
                    if selection_active:
                        user_text = user_text[:selection_beg] + user_text[selection_end:]
                        cur_pos = selection_beg
                        (selection_active, selection_beg, selection_end) = (False, -1, -1)
                    elif cur_pos > 0:
                        user_text = user_text[:cur_pos] + user_text[cur_pos+1:]
                elif event.key == pygame.K_LEFT:
                    prev_pos = cur_pos
                    cur_pos -= 1
                    if cur_pos < 0:
                        cur_pos = 0
                    if mods & pygame.KMOD_CTRL:
                        while cur_pos > 0 and user_text[cur_pos-1] != ' ':
                            cur_pos -= 1
                    if mods & pygame.KMOD_SHIFT:
                        selection_active = True
                        if selection_end == -1:
                            selection_end = prev_pos
                            selection_beg = cur_pos
                        else:
                            if selection_beg == prev_pos:
                                selection_beg = cur_pos
                            else:
                                selection_end = cur_pos
                    else:
                        (selection_active, selection_beg, selection_end) = (False, -1, -1)
                elif event.key == pygame.K_RIGHT:
                    prev_pos = cur_pos
                    cur_pos += 1
                    if cur_pos > len(user_text):
                        cur_pos = len(user_text)
                    if mods & pygame.KMOD_CTRL:
                        while cur_pos < len(user_text) and user_text[cur_pos] != ' ':
                            cur_pos += 1
                    if mods & pygame.KMOD_SHIFT:
                        selection_active = True
                        if selection_end == -1:
                            selection_end = cur_pos
                            selection_beg = prev_pos
                        else:
                            if selection_end == prev_pos:
                                selection_end = cur_pos
                            else:
                                selection_beg = cur_pos
                    else:
                        (selection_active, selection_beg, selection_end) = (False, -1, -1)
                elif event.key == pygame.K_UP:
                    prev_pos = cur_pos
                    if cur_pos - max_smbs >= 0:
                        cur_pos -= max_smbs
                    else:
                        cur_pos = 0
                    if mods & pygame.KMOD_SHIFT:
                        selection_active = True
                        if selection_end <= cur_pos or selection_beg == -1:
                            selection_end = prev_pos
                        selection_beg = cur_pos
                    else:
                        (selection_active, selection_beg, selection_end) = (False, -1, -1)
                elif event.key == pygame.K_DOWN:
                    prev_pos = cur_pos
                    if cur_pos + max_smbs < len(user_text):
                        cur_pos += max_smbs
                    else:
                        cur_pos = len(user_text)
                    if mods & pygame.KMOD_SHIFT:
                        selection_active = True
                        if selection_beg >= cur_pos or selection_beg == -1:
                            selection_beg = prev_pos
                        selection_end = cur_pos
                    else:
                        (selection_active, selection_beg, selection_end) = (False, -1, -1)
                elif event.key == pygame.K_HOME:
                    prev_pos = cur_pos
                    cur_pos = 0
                    if mods & pygame.KMOD_SHIFT:
                        selection_active = True
                        if selection_end <= cur_pos or selection_beg == -1:
                            selection_end = prev_pos
                        selection_beg = cur_pos
                    else:
                        (selection_active, selection_beg, selection_end) = (False, -1, -1)
                elif event.key == pygame.K_END:
                    prev_pos = cur_pos
                    cur_pos = len(user_text)
                    if mods & pygame.KMOD_SHIFT:
                        selection_active = True
                        if selection_beg >= cur_pos or selection_beg == -1:
                            selection_beg = prev_pos
                        selection_end = cur_pos
                    else:
                        (selection_active, selection_beg, selection_end) = (False, -1, -1)
                elif event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                    active = False
                elif mods & pygame.KMOD_CTRL and event.key == pygame.K_c:
                    if selection_active:
                        s = user_text[selection_beg:selection_end]
                        scrap.put(pygame.SCRAP_TEXT, s.encode("utf-8"))
                elif mods & pygame.KMOD_CTRL and event.key == pygame.K_a:
                    (selection_active, selection_beg, selection_end) = (True, 0, len(user_text))
                elif mods & pygame.KMOD_CTRL and event.key == pygame.K_v:
                    for t in scrap.get_types():
                        if t == 'text/plain':
                            r = scrap.get(t)
                            if r and len(r) > 5000:
                                pass
                                #print(f"Type {t} : (large {len(r)} byte buffer)")
                            elif r is None:
                                pass
                                #print(f"Type {t} : None")
                            else:
                                #print(f"Type {t} : '{r.decode('ascii', 'ignore')}'")
                                clipboard_text = r.decode('ascii', 'ignore')
                                clipboard_text = re.sub("\s+", ' ', clipboard_text)
                                clipboard_text = re.sub(f"[^{good_chars}]", '', clipboard_text)
                                print(clipboard_text)
                                if selection_active:
                                    user_text = user_text[:selection_beg] + user_text[selection_end:]
                                    cur_pos = selection_beg
                                    (selection_active, selection_beg, selection_end) = (False, -1, -1)
                                user_text = user_text[0:cur_pos] + clipboard_text + user_text[cur_pos:]
                                cur_pos += len(clipboard_text)
                else:
                    newchar = event.unicode
                    if(re.match(f"[{good_chars}]", newchar)):
                        if selection_active:
                            user_text = user_text[:selection_beg] + user_text[selection_end:]
                            cur_pos = selection_beg
                            (selection_active, selection_beg, selection_end) = (False, -1, -1)

                        user_text = user_text[0:cur_pos] + event.unicode + user_text[cur_pos:]
                        cur_pos += 1

       
        redraw()
      
        if active:
            color = color_active
        else:
            color = color_passive
            
        pygame.draw.rect(screen, color, input_rect)

        windows_min = int(cur_pos / max_smbs) * max_smbs - (max_lines-1) * max_smbs
        if windows_min < 0:
            windows_min = 0
        if window_start < windows_min:
            window_start = windows_min
        if window_start > cur_pos:
            window_start -= max_smbs

        window_end = window_start + max_lines * max_smbs

        if old_style_cursor:
            current_text = user_text[window_start:cur_pos] + cur_smb + user_text[cur_pos:window_end]
        else:
            current_text = user_text[window_start:window_end]

        ii = 0
        for i in range(0, len(current_text), max_smbs):
             if old_style_cursor:
                 corr1 = 0 if i <= int(cur_pos/max_smbs)*max_smbs else 1
                 corr2 = 1 if i >= int(cur_pos/max_smbs)*max_smbs else 0
             else:
                 corr1 = 0
                 corr2 = 0
             text_surface = base_font.render(current_text[i + corr1 : i+max_smbs+corr2], True, (255, 255, 255))
             screen.blit(text_surface, (input_rect.x+5, input_rect.y+5 + ii * 20))
             ii += 1

        if time.time() % 1 > 0.5:
            window_cur_state = cur_pos - window_start
            cur_x = input_rect.x+5 + int(window_cur_state % max_smbs) * 12
            cur_y = input_rect.y+5 + int(window_cur_state / max_smbs) * 20
            cursor = pygame.Rect(cur_x, cur_y, 3, 20)
            pygame.draw.rect(screen, (0,0,0), cursor)

        for i in range(max_lines):
            for j in range(max_smbs):
                check_pos = i * max_smbs + j + window_start
                if check_pos >= selection_beg and check_pos < selection_end:
                    cur_x = input_rect.x+5 + j * 12
                    cur_y = input_rect.y+5 + i * 20
                    cursor = pygame.Rect(cur_x, cur_y+18, 12, 2)
                    pygame.draw.rect(screen, (0,0,0), cursor)

        input_rect.w = x2 - x1
        input_rect.h = y2 - y1
        
        pygame.display.flip()
        
        clock.tick(60)

    return user_text
