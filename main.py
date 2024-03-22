import pygame
from pygame import mixer
pygame.init()
screen_size = pygame.display.Info()
width = screen_size.current_w
height = screen_size.current_h
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("UnderArad")
font = pygame.font.Font('freesansbold.ttf', 32)

try:
    icon = pygame.image.load("images/icon.jpg").convert()
except:
    raise FileNotFoundError("File: \"icon.jpg\" not found!")
else:
    pygame.display.set_icon(icon)

wallpaper = pygame.display.set_mode((width, height))
try:
    picture = pygame.image.load("images/background.jpeg").convert()
except:
    raise FileNotFoundError("File: \"background.jpeg\" not found!")
else:
    picture = pygame.transform.scale(picture, (width, height))
    rect = picture.get_rect()
    rect = rect.move((0, 0))

try:
    player_image = pygame.image.load("images/arad_default.png")
except:
    raise FileNotFoundError("File: \"arad_default.png\" not found!")

try:
    wall_image = pygame.image.load("images/wall1.png").convert()
except:
    raise FileNotFoundError("File: \"wall1.png\" not found!")


class Player:
    def __init__(self, inName):
        """
            variables:
                went_left : whether the last movement was towards left or not
                x/y : begging position
                horizontal_movement: total movement in the X axis (left + right)
                verticaal_movement: total movement in the Y axis (up + down)
        """
        self.width = player_image.get_width()
        self.height = player_image.get_height()
        self.health = 100
        self.name = inName
        self.went_left = False
        self.speed = 3
        self.x = 100
        self.y = 100
        self.horizontal_movement = 0
        self.vertical_movement = 0
        self.left = 0
        self.right = 0
        self.down = 0
        self.up = 0
        
    def display(self, image):
        """
            attrs:
                image : player's image
        """
        self.horizontal_movement = -self.left + self.right
        self.vertical_movement = -self.up + self.down
        self.x += self.horizontal_movement
        self.y += self.vertical_movement
        if self.horizontal_movement > 0:
            pass
        elif self.horizontal_movement < 0 or self.went_left: 
            # if the player is going towards the left side or it's last movement was towards the left side
            image = pygame.transform.flip(image, True, False)
        if self.x < 0 or self.x + image.get_width() > width:
            self.x -= self.horizontal_movement
        if self.y < 0 or self.y + image.get_height() > height:
            self.y -= self.vertical_movement
        screen.blit(image, (self.x, self.y))
    
    def e_button_action(self):
        pass


class Wall:
    def __init__(self, image_file_location, position:tuple):
        self.wall_image = image_file_location
        self.x = position[0]
        self.y = position[1]
        self.player_is_above = False
        self.player_is_at_left = False
        
    def display(self, player_obj):
        """
            This is the whole wall's collision system. (It was so fucking hard to achieve so I deserve an applause)
        """
        if player_obj.y + player_obj.height < self.y + self.wall_image.get_height()/2:
            self.player_is_above = True
        else:
            self.player_is_above = False
        if player_obj.x + player_obj.width < self.y + self.wall_image.get_width()/2:
            self.player_is_at_left = True
        else:
            self.player_is_at_left = False

        if player_obj.x + player_obj.width/2 > self.x + 5 and player_obj.x + player_obj.width/2 + 5 < self.x + self.wall_image.get_width():
            if player_obj.y + player_obj.height > self.y and player_obj.y + player_obj.height < self.y + self.wall_image.get_height():
                if self.player_is_above:
                    player_obj.y -= player_obj.speed
                if not self.player_is_above:
                    player_obj.y += player_obj.speed
        if player_obj.y + player_obj.height > self.y + 5 and player_obj.y + player_obj.height + 5 < self.y + self.wall_image.get_height():
            if player_obj.x + player_obj.width/2 > self.x and player_obj.x + player_obj.width/2 < self.x + self.wall_image.get_width():
                if self.player_is_at_left:
                    player_obj.x -= player_obj.speed
                if not self.player_is_at_left:
                    player_obj.x += player_obj.speed
        screen.blit(self.wall_image, (self.x, self.y))


class Button:
    def __init__(self, image_file_location, hover_image_file_location):
        """
            attrs: 
                location : a tuple containing the X and Y components of the button
                image_file_location : default button's image
                hover_image_file_location : hovered button's image
        """
        self.file_loc = image_file_location
        self.hover_image = pygame.image.load(hover_image_file_location).convert()
        self.button_image = pygame.image.load(image_file_location).convert()
        # the center of the button is placed at the given location, not the top left corner of it.
        
    def blit_button(self, location):
        """
            blits the image on the screen, capable of changing while hovered
        """
        self.location = (location[0] - self.button_image.get_width() / 2, location[1] - self.button_image.get_height() / 2)
        mouse_position = pygame.mouse.get_pos()
        image = self.button_image
        if mouse_position[0] >= self.location[0] and \
                mouse_position[0] <= self.location[0] + self.button_image.get_width() and \
                mouse_position[1] >= self.location[1] and \
                mouse_position[1] <= self.location[1] + self.button_image.get_height():
            image = self.hover_image # if it was hovered
        screen.blit(image, (self.location[0], self.location[1], image.get_width(), image.get_height()))
    
    def clicked(self):
        mouse_position = pygame.mouse.get_pos()
        if mouse_position[0] >= self.location[0] and \
                mouse_position[0] <= self.location[0] + self.button_image.get_width() and \
                mouse_position[1] >= self.location[1] and \
                mouse_position[1] <= self.location[1] + self.button_image.get_height():
            return True # if it was clicked
        else:
            return False


def main_menu():
    decision = "None"
    pygame.display.set_caption("Menu")
    at_menu = True
    start_button = Button("images/start_button.png", "images/start_button_hover.png")
    options_button = Button("images/options_button.png", "images/options_button_hover.png")
    exit_button = Button("images/exit_button.png", "images/exit_button_hover.png")
    while at_menu:
        screen.fill("black")
        start_button.blit_button((width/2, height/2 - 110))
        options_button.blit_button((width/2, height/2))
        exit_button.blit_button((width/2, height/2 + 110))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                at_menu = False
                decision = "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    at_menu = False
                    decision = "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.clicked():
                    at_menu = False
                    decision = "play"
                if options_button.clicked():
                    at_menu = False
                    decision = "options"
                if exit_button.clicked():
                    at_menu = False
                    decision = "quit"
        pygame.display.update()
    return decision


def options():
    at_options = True
    while at_options:
        screen.fill("black")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                at_options = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    at_options = False
        pygame.display.update()
    
    return "menu"


def gameplay():
    running = True
    player_name = "Arad"
    player = Player(player_name)
    wall1 = Wall(wall_image, (500, 500))
    while running:
        screen.fill((194, 8, 6)) # default color
        wallpaper.blit(picture, rect)
        wall1.display(player)
        player.display(player_image)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_a:
                    player.left = player.speed
                    player.went_left = True
                if event.key == pygame.K_d:
                    player.right = player.speed
                    player.went_left = False
                if event.key == pygame.K_w:
                    player.up = player.speed
                if event.key == pygame.K_s:
                    player.down = player.speed

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    player.left = 0
                if event.key == pygame.K_d:
                    player.right = 0
                if event.key == pygame.K_s:
                    player.down = 0
                if event.key == pygame.K_w:
                    player.up = 0
        pygame.display.update()

App_running = True
while App_running:
    decision = main_menu()
    if decision == "options":
        options()
    elif decision == "play": 
        gameplay()
    elif decision == "options":
        options()
    elif decision == "quit":
        App_running = False