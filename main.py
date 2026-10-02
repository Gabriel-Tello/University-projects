import pygame
import sys, random, colorsys

screen_width, screen_height = 640, 640
FPS = 60
delta_time = 0.016  # Approximate time per frame at 60 FPS

# ---------------------------------------------------------------------------------------  Game  -----------------------------------------------------------------------------------------

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Proyectos!")
        pygame.display.set_icon(pygame.image.load("icon.ico"))
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()

        self.gameStateManager = GameStateManager("start")
        self.estrellas = []
        # Dibujar 50 estrellas iniciales
        for i in range(50):
            self.estrellas.append([[random.uniform(0, 640), random.uniform(0, 640)], [-0.3, 0.8], random.uniform(0, 1)])
        self.music = MusicManager()
        self.start = Start(self.screen, self.gameStateManager, self.estrellas, self.music)
        self.music.play("assets/sound/Chiptune.mp3")
        self.options = Options(self.screen, self.gameStateManager, self.music, self.estrellas)

        self.states = {
            "start": self.start,
            "options": self.options
        }
        
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            self.states[self.gameStateManager.get_state()].run()

            pygame.display.flip()
            # Control the frame rate
            delta_time = self.clock.tick(FPS) / 1000
            delta_time = max(0.001, min(0.1, delta_time))
        pygame.quit()
        sys.exit()

# ---------------------------------------------------------------------------------------  Start  -----------------------------------------------------------------------------------------

class Start:
    def __init__(self, display, gameStateManager, estrellas, music):
        self.display = display
        self.gameStateManager = gameStateManager
        self.clock = pygame.time.Clock()
        self.estrellas = estrellas
        self.music = music

    def run(self):
        anim = 0
        
        # Load fonts
        title_font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", size=30)
        main_font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", size=25)
        tiny_font = pygame.font.Font("assets/fonts/Tiny5-Regular.ttf", size=25)

        # Load arrow images
        flecha1 = pygame.image.load('assets/sprites/Flecha1.png').convert_alpha()
        flecha1 = pygame.transform.scale(flecha1, (flecha1.get_width() * 3, flecha1.get_height() * 3))
        flecha2 = pygame.image.load('assets/sprites/Flecha2.png').convert_alpha()
        flecha2 = pygame.transform.scale(flecha2, (flecha2.get_width() * 3, flecha2.get_height() * 3))

        select_s = pygame.mixer.Sound("assets/sound/Select.wav")

        titles = ["P", "R", "O", "Y", "E", "C", "T", "O", "S", "!"]
        titles_render = []
        for i in range(len(titles)):
            titles_render.append(title_font.render(titles[i], False, (255, 255, 255)))
        title_y = [45, 47, 49, 51, 53, 55, 57, 59, 61, 63]
        title_down = [True] * len(titles)
        hue_offset = 0

        running = True
        while running:
            self.display.fill((0, 0, 0))

            select_s.set_volume(self.music.sfx_volume)

            # Draw stars
            if anim % 15 == 0:
                self.estrellas.append([[random.randint(0, 900), -1], [-0.3, 0.8], random.uniform(0, 2)])

            for estrella in self.estrellas:
                estrella[0][0] += estrella[1][0] - estrella[2]
                estrella[0][1] += estrella[1][1] + estrella[2]
                pygame.draw.rect(self.display, (255, 255, 255), (estrella[0][0], estrella[0][1], 4, 4))
                if estrella[0][1] > 640:
                    self.estrellas.remove(estrella)

            # Get the mouse position
            mpos = pygame.mouse.get_pos()
            # Get the text surfaces
            options = main_font.render("Opciones", False, (255, 255, 255))
            quit = main_font.render("Salir", False, (255, 255, 255))
            credits = tiny_font.render("Gabriel Tello - 2026", False, (255, 255, 255))
             # Proyectos! / 2026
            album = tiny_font.render("01 - Album de figuritas simulator 1984", False, (255, 255, 255))
            diez_mil = tiny_font.render("02 - 10 Mil", False, (255, 255, 255))
            incendio = tiny_font.render("03 - Incendio Forestal simulator 1986", False, (255, 255, 255))

            # Draw text
            self.display.blit(credits, (636 - credits.get_width(), 638 - credits.get_height()))
            self.display.blit(options, (100, 500))
            self.display.blit(quit, (540 - quit.get_width(), 500))
             # Proyectos! / 2026
            self.display.blit(album, (100, 150))
            self.display.blit(diez_mil, (100, 200))
            self.display.blit(incendio, (100, 250))
             # Title
            for i in range(len(titles)):
                self.display.blit(titles_render[i], (320 - (len(titles) * titles_render[i].get_width()) / 2 + i * titles_render[i].get_width(), title_y[i]))
    
                if title_y[i] <= 45:
                    title_down[i] = True
                elif title_y[i] >= 65:
                    title_down[i] = False
                if title_down[i]:
                    title_y[i] += 0.5
                else:
                    title_y[i] -= 0.5

                # Hue goes from 0.0 to 1.0
                hue = (hue_offset + i * 0.07) % 1.0

                # Convert HSV/HLS-style color to RGB
                r, g, b = colorsys.hsv_to_rgb(hue, 1, 1)

                # Convert from 0-1 to 0-255
                color = (
                    int(r * 255),
                    int(g * 255),
                    int(b * 255)
                )
                
                titles_render[i] = title_font.render(titles[i], False, color)

            hue_offset = (hue_offset + 0.005) % 1.0

            # Buttons
            options_button = pygame.Rect(100, 500, options.get_width(), options.get_height())
            quit_button = pygame.Rect(540 - quit.get_width(), 500, quit.get_width(), quit.get_height())
            album_button = pygame.Rect(100, 150, album.get_width(), album.get_height())
            diez_mil_button = pygame.Rect(100, 200, diez_mil.get_width(), diez_mil.get_height())
            incendio_button = pygame.Rect(100, 250, incendio.get_width(), incendio.get_height())

            # Check for mouse collision with buttons
            if options_button.collidepoint(mpos):
                if anim % 60 < 40:
                    self.display.blit(flecha2, (70, 502))
                    options = main_font.render("Opciones", False, (217, 87, 99))
                    self.display.blit(options, (100, 500))
                else:
                    self.display.blit(flecha1, (70, 502))
                    options = main_font.render("Opciones", False, (172, 50, 50))
                    self.display.blit(options, (100, 500))
                if pygame.mouse.get_pressed()[0]:
                    self.gameStateManager.set_state("options")
                    select_s.play(0)
                    running = False

            if quit_button.collidepoint(mpos):
                if anim % 60 < 40:
                    self.display.blit(flecha2, (385, 502))
                    quit = main_font.render("Salir", False, (217, 87, 99))
                    self.display.blit(quit, (540 - quit.get_width(), 500))
                else:
                    self.display.blit(flecha1, (385, 502))
                    quit = main_font.render("Salir", False, (172, 50, 50))
                    self.display.blit(quit, (540 - quit.get_width(), 500))
                if pygame.mouse.get_pressed()[0]:
                    select_s.play(0)
                    pygame.quit()
                    sys.exit()

            if album_button.collidepoint(mpos):
                if anim % 60 < 40:
                    self.display.blit(flecha2, (70, 152))
                    album = tiny_font.render("01 - Album de figuritas simulator 1984", False, (217, 87, 99))
                    self.display.blit(album, (100, 150))
                else:
                    self.display.blit(flecha1, (70, 152))
                    album = tiny_font.render("01 - Album de figuritas simulator 1984", False, (172, 50, 50))
                    self.display.blit(album, (100, 150))


            if diez_mil_button.collidepoint(mpos):
                if anim % 60 < 40:
                    self.display.blit(flecha2, (70, 202))
                    diez_mil = tiny_font.render("02 - 10 Mil", False, (217, 87, 99))
                    self.display.blit(diez_mil, (100, 200))
                else:
                    self.display.blit(flecha1, (70, 202))
                    diez_mil = tiny_font.render("02 - 10 Mil", False, (172, 50, 50))
                    self.display.blit(diez_mil, (100, 200))


            if incendio_button.collidepoint(mpos):
                if anim % 60 < 40:
                    self.display.blit(flecha2, (70, 252))
                    incendio = tiny_font.render("03 - Incendio Forestal simulator 1986", False, (217, 87, 99))
                    self.display.blit(incendio, (100, 250))
                else:
                    self.display.blit(flecha1, (70, 252))
                    incendio = tiny_font.render("03 - Incendio Forestal simulator 1986", False, (172, 50, 50))
                    self.display.blit(incendio, (100, 250))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if album_button.collidepoint(mpos):
                        print("01 - Album de figuritas simulator 1984 selected")
                        select_s.play(0)
                    if pygame.mouse.get_pressed()[0]:
                        print("02 - 10 Mil selected")
                        select_s.play(0)
                    if pygame.mouse.get_pressed()[0]:
                        print("03 - Incendio Forestal simulator 1986 selected")
                        select_s.play(0)

            anim += 1
            anim %= 600

            pygame.display.flip()
            # Control the frame rate
            delta_time = self.clock.tick(FPS) / 1000
            delta_time = max(0.001, min(0.1, delta_time))

# ---------------------------------------------------------------------------------------  Options  -----------------------------------------------------------------------------------------
        
class Options:
    def __init__(self, display, gameStateManager, music, estrellas):
        self.display = display
        self.gameStateManager = gameStateManager
        self.music = music
        self.clock = pygame.time.Clock()
        self.estrellas = estrellas
        
    def run(self):
        
        anim = 0
        select_s = pygame.mixer.Sound("assets/sound/Select.wav")
        circle = pygame.image.load("assets/sprites/circle.png")
        circle = pygame.transform.scale(circle, (circle.get_width() * 1.7, circle.get_height() * 1.7))

        running = True
        while running:
            
            # Load fonts
            title_font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", size=30)
            main_font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", size=25)
            tiny_font = pygame.font.Font("assets/fonts/Tiny5-Regular.ttf", size=25)

            select_s.set_volume(self.music.sfx_volume)

            mpos = pygame.mouse.get_pos()

            self.display.fill((0, 0, 0))

            # Draw stars
            if anim % 15 == 0:
                self.estrellas.append([[random.randint(0, 900), -1], [-0.3, 0.8], random.uniform(0, 2)])

            for estrella in self.estrellas:
                estrella[0][0] += estrella[1][0] - estrella[2]
                estrella[0][1] += estrella[1][1] + estrella[2]
                #estrella[0][1] += estrella[2]
                pygame.draw.rect(self.display, (255, 255, 255), (estrella[0][0], estrella[0][1], 4, 4))
                if estrella[0][1] > 640:
                    self.estrellas.remove(estrella)

            options_title = title_font.render("Opciones", False, (255, 255, 255))
            self.display.blit(options_title, (50, 50))

            mute_text = main_font.render("Mute", False, (255, 255, 255))
            self.display.blit(mute_text, (120, 120))

            Música_text = main_font.render("Música ", False, (255, 255, 255))
            self.display.blit(Música_text, (90, 155))

            sfx_text = main_font.render("SFX", False, (255, 255, 255))
            self.display.blit(sfx_text, (90, 190))

            slider = main_font.render("[          ]", False, (255, 255, 255))
            self.display.blit(slider, (90 + Música_text.get_width(), 155))
            self.display.blit(slider, (90 + Música_text.get_width(), 190))

            barra = main_font.render("|", False, (255, 255, 255))
            
            music_slider = pygame.rect.Rect(90 + Música_text.get_width(), 155, slider.get_width(), slider.get_height())
            sfx_slider = pygame.rect.Rect(90 + Música_text.get_width(), 190, slider.get_width(), slider.get_height())

            music_bars = int(self.music.volume * 10)
            sfx_bars = int(self.music.sfx_volume * 10)

            for i in range(music_bars):
                self.display.blit(barra, (90 + Música_text.get_width() + 25 * (i + 1), 155))
            for i in range(sfx_bars):
                self.display.blit(barra, (90 + Música_text.get_width() + 25 * (i + 1), 190))

            if sfx_slider.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                self.music.set_sfx_volume((mpos[0] - (90 + Música_text.get_width())) / 265)     
                if self.music.previous_sfx_volume != self.music.sfx_volume:
                    select_s.play(0)
            if music_slider.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                self.music.set_volume((mpos[0] - (90 + Música_text.get_width())) / 265)
                if self.music.previous_volume != self.music.volume:
                    select_s.play(0)

            mute_button = pygame.Rect(80, 122, 20, 20)
            
            if mute_button.collidepoint(mpos):
                pygame.draw.rect(self.display, (255, 255, 255), mute_button, 3)
                if self.music.muted:
                    self.display.blit(circle, (84, 126))
                if pygame.mouse.get_pressed()[0]:
                    pygame.draw.rect(self.display, (217, 87, 99), mute_button, 4)
            elif not self.music.muted:
                pygame.draw.rect(self.display, (255, 255, 255), mute_button, 2)
            else:
                pygame.draw.rect(self.display, (255, 255, 255), mute_button, 2)
                self.display.blit(circle, (84, 126))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.gameStateManager.set_state(self.gameStateManager.get_previous_state())
                        running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if mute_button.collidepoint(mpos):
                        select_s.play(0)
                        self.music.toggle_mute()          

            
            pygame.display.flip()
            # Control the frame rate
            delta_time = self.clock.tick(FPS) / 1000
            delta_time = max(0.001, min(0.1, delta_time))
            
            anim += 1
            anim %= 600



class GameStateManager:
    def __init__(self, current_state):
        self.current_state = current_state
        self.previous_state = None
    def get_state(self):
        return self.current_state
    def set_state(self, state):
        self.previous_state = self.current_state
        self.current_state = state
    def get_previous_state(self):
        return self.previous_state

class MusicManager:
    def __init__(self):
        self.muted = False
        self.volume = 0.3
        self.previous_volume = None
        self.sfx_volume = 0.5
        self.previous_sfx_volume = None

        pygame.mixer.music.set_volume(self.volume)

    def play(self, filename):
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play(-1)

    def toggle_mute(self):
        self.muted = not self.muted

        if self.muted:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

    def set_volume(self, v):
        self.previous_volume = self.volume
        self.volume = (int(v * 10))/10
        pygame.mixer.music.set_volume(self.volume)
    
    def set_sfx_volume(self, v):
        self.previous_sfx_volume = self.sfx_volume
        self.sfx_volume = (int(v * 10))/10
        self.sfx_volum = min(self.sfx_volume, 1)


if __name__ == "__main__":
    game = Game()
    game.run()

"""

x = 0

moving = False

while running:

    # Fill the screen with black
    screen.fill((0, 0, 0))
    #screen.fill((255, 255, 255))

    screen.blit(duck_img, (x, 30))

    # Create a hitbox for the duck
    hitbox = pygame.Rect(x, 30, duck_img.get_width(), duck_img.get_height())
   
    # Create a target rectangle
    target = pygame.Rect(300, 0, 160, 200)
    # Check for collision between the hitbox or mouse and the target rectangle
    collision = hitbox.colliderect(target)
    m_collision = target.collidepoint(mpos)
    # Draw the target rectangle with a color based on collision status
    rectangulo = pygame.draw.rect(screen, (255 * collision, 255 * m_collision, 0), target)


    if moving:
        x += 50 * delta_time


    # Handle events (like key presses, exiting, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                moving = True
            if event.key == pygame.K_f:
                sound.play()
                target = None
                rectangulo = None
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                 moving = False


    # Update the display
    pygame.display.flip()
"""

pygame.quit()

