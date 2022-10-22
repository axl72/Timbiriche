from audioop import mul
from nis import match
import pygame
import sys
import os
from core.button import Button
from core.model import House, Circle, Cable
from core.table import Table

colors = {"blue": (88, 114, 138), 
        "grey": (200, 189, 183),
        "white": (255, 255, 255),
        "sky": (251, 255, 255),
        "dark blue": (11, 46, 89),
        "red": (204, 0, 102)}

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 900))
        self.resources = "assets"
        self.name_font = "Quarterback.otf"
        self.status = "menu"
        self.clock = pygame.time.Clock()
        self.get_mouse_pos = pygame.mouse.get_pos
        self.click_event = pygame.mouse.get_pressed
        self.houses = pygame.sprite.Group()
        self.current_player = True
        self.table = Table(7, 7)
        self.cordenates_circles = {"x": (100, 250, 400, 550, 700, 850, 1000, 1150), "y": (80, 180, 280, 380, 480, 580, 680, 780)}
        self.cordenates_houses = {"x": (145, 295, 445, 595, 745, 895, 1045), "y": (105, 205, 305, 405, 505, 605, 705)}
        self.circles_list = [[Circle(x, y, (row, column)) for column, y in enumerate(self.cordenates_circles["y"])] for row, x in enumerate(self.cordenates_circles["x"])]
        self.houses_list = [[House((x, y)) for x in self.cordenates_houses["x"]] for y in self.cordenates_houses["y"]]
        self.houses.add(house for house in self.houses_list)
        self.clicked_circles = set()
        self.cordenates = {
            
        }
    
    def __draw_line__(self, x, y, status):
        if status == 1:
            return

        cordenates = {2: ((x, y), (x, y+1)), 
            3: ((x, y), (x+1, y)),
            5: ((x+1, y), (x+1, y+1)),
            7: ((x, y+1), (x+1, y +1))}
        
        for multiple in (2, 3, 5, 7):
            if not status % multiple:
                a, b = cordenates[multiple]
                x1, y1 = a
                x2, y2 = b
                circle_start = self.circles_list[x1][y1]
                circle_end = self.circles_list[x2][y2]
                cordenate_start = circle_start.get_cordenates()
                cordenate_end = circle_end.get_cordenates()
                pygame.draw.line(self.screen, (0, 0, 0), cordenate_start, cordenate_end, 2)
    

    def __logic_game__(self, cordenates):
        if len(self.clicked_circles) == 0:
            self.clicked_circles.add(cordenates)
        
        elif len(self.clicked_circles) == 1:
            x1, y1 = list(self.clicked_circles)[0]
            x2, y2 = cordenates
            if (abs(x1 - x2) == 1 and y1 == y2) or ((abs(y1 - y2) == 1 and x1 == x2)): 
                self.clicked_circles.add(cordenates)

        if len(self.clicked_circles) == 2:
            x1, y1 = self.clicked_circles.pop()
            x2, y2 = self.clicked_circles.pop()
            print((x1, y1), " & ", (x2, y2))

            is_border =  True if ((x1 == 0 and x2 == 0) or (y1 == 0 and y2 == 0)) or ((x1 == 7 and x2 == 7) or (y1 == 7 and y2 == 7)) else False

            if is_border:
                if y1 != 7 and y2 != 7 and x1 != 7 and x2 != 7:
                    index_houses = (int(abs(x1 + x2)/2), int(y1)) if abs(x1 - x2) == 1 and y1 == y2 else (int(x1), int(abs(y1 + y2)/2))
                else :
                    index_houses = (int(abs(x1 + x2)/2), int(y1-1)) if abs(x1 - x2) == 1 and y1 == y2 else (int(x1-1), int(abs(y1 + y2)/2))
                value = 2 if y1 != y2 and (x1 != 7 and x2 != 7) else 5 if y1 != y2 and (x1 == 7 or x2 == 7) else 3 if x1 != x2 and (y1 == 0 or y2 == 0) else 7
                print(index_houses)
                self.table.set_cable(index_houses[0], index_houses[1], value)
                
                self.current_player = not self.current_player    
                return 

            index_houses = [(int(abs(x1+x2)/2), int(y1)), (int(abs(x1+x2)/2), int(y1-1))] if (abs(x1 - x2) == 1 and y1 == y2) else [(int(x1), (int(abs(y1+y2)/2))), (int(x1-1), int(abs(y1+y2)/2))]

            values = (2, 5) if y1 != y2 else (3, 7)

            a1, b1 = index_houses[0]
            a2, b2 = index_houses[1]
            print(index_houses)
            if a1 - a2 > 0 or b1 - b2 > 0:
                self.table.set_cable(index_houses[0][0], index_houses[0][1], values[0])
                self.table.set_cable(index_houses[1][0], index_houses[1][1], values[1])
            elif a1 - a2 < 0 or b1 - b2 < 0:
                self.table.set_cable(index_houses[0][0], index_houses[0][1], values[1])
                self.table.set_cable(index_houses[1][0], index_houses[1][1], values[0])

            self.current_player = not self.current_player    
        

    def game(self):
        self.screen.fill(colors["blue"])

        for x, row in enumerate(self.table.setup):
            for y, value in enumerate(row):
                self.__draw_line__(x, y, value)

        [circle.draw(self.screen) for row in self.circles_list for circle in row]
        self.houses.draw(self.screen) 
        
        cordenates = self.get_mouse_pos()

        for row in self.circles_list:
            for circle in row:
                if circle.is_point_in(cordenates):
                    if self.click_event()[0]:
                        self.__logic_game__(circle.get_indexes())

    def start_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        #self.status = "menu"
                        self.clicked_circles.clear()

                if event.type == pygame.QUIT:
                    sys.exit()

            if self.status == "menu":
                self.menu()
            
            if self.status == "game":
                self.game()

            pygame.display.flip()
            self.clock.tick(10)


    def menu(self):
        """method to show game menu"""
        self.screen.fill(colors["blue"])

     
        grey_color = colors["grey"]
        path_font = os.path.join(self.resources, self.name_font)
        big_font = pygame.font.Font(path_font, 50)
        small_font = pygame.font.Font(path_font, 20)

        welcome_text = big_font.render("Cable vs ADSL", True, grey_color)
        created_by = small_font.render("Created by axl72", True, grey_color)

     

        img = pygame.image.load(os.path.join(self.resources, "Options Rect.png"))

        play_button = Button(image=img, pos=(570, 350), text_input="Play", font=small_font, base_color="#d7fcd4", hovering_color="Red")
        options_button = Button(image=img, pos=(570, 500), text_input="Options", font=small_font, base_color="#d7fcd4", hovering_color="Red")

        for button in [play_button, options_button]:
             button.changeColor(pygame.mouse.get_pos())
             button.update(self.screen)

        self.screen.blit(welcome_text, 
                      ((self.screen.get_width() - welcome_text.get_width()) // 2, 
                      150))
        # show credit text
        self.screen.blit(created_by, 
                      ((self.screen.get_width() - created_by.get_width()) // 2, 
                      self.screen.get_height() - created_by.get_height() - 100))

        if play_button.checkForInput(self.get_mouse_pos()):
            if self.click_event()[0]:
                self.status = "game"

        if options_button.checkForInput(self.get_mouse_pos()):
            if self.click_event()[0]:
                self.status = "options"
        
if __name__ == "__main__":
    game = Game()
    game.start_game()
