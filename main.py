import pygame, sys, time

pygame.init()
clock = pygame.time.Clock()

#DISPLAY WINDOW
screenx = 800
screeny = 400
screen = pygame.display.set_mode((screenx, screeny))


class Button(
        pygame.sprite.Sprite
):  #takes care of all the buttons in the program (even if they aren't supposed to be pressed)

    def __init__(self, image_path, pos_x, pos_y, scale):
        super().__init__()
        self.image = pygame.image.load(image_path)
        width = self.image.get_width()
        height = self.image.get_height()
        self.image = pygame.transform.scale(
            self.image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect(center=(pos_x, pos_y))
        self.clicked = False

    def draw(self):
        pos = pygame.mouse.get_pos()
        action = False

        if self.rect.collidepoint(
                pos):  #checks to see if the cursor is on the button
            #print("hover")

            if pygame.mouse.get_pressed(
            )[0] and not self.clicked:  #self.clicked makes sure you can't just hold down the mouse button
                #print("clicked")
                self.clicked = True
                action = True

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action  #boolean for executing an action after the button is pressed


def post_game(p1Win):

    pygame.display.set_caption("Game Over")
    background_surface = pygame.image.load('start_background.png')
    background_surface = pygame.transform.scale(background_surface,
                                                (screenx, screeny))
    pygame.mouse.set_visible(False)

    #CLASSES
    class Cursor(pygame.sprite.Sprite
                 ):  #class for displaying the in-game cursor

        def __init__(self, image_path):
            super().__init__()
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.image, (20, 20))
            self.rect = self.image.get_rect(topleft=(screenx / 2, screeny / 2))

        def update(self):

            self.rect.center = pygame.mouse.get_pos()

    class Model1(
            pygame.sprite.Sprite
    ):  #class for animating and displaying the green dragon sprite

        def __init__(self, pos):
            super().__init__()
            self.sprites = []  #list of frames for the animation
            self.sprites.append(
                pygame.transform.scale(pygame.image.load('frame-1.png'),
                                       (123, 90)))
            self.sprites.append(
                pygame.transform.scale(pygame.image.load('frame-2.png'),
                                       (123, 90)))
            self.sprites.append(
                pygame.transform.scale(pygame.image.load('frame-3.png'),
                                       (123, 90)))

            self.current_sprite = 0
            self.image = self.sprites[self.current_sprite]

            self.dead_sprite = False  #boolean for determining if the dragon should be dead or flying

            #RECT
            self.rect = self.image.get_rect()
            self.rect.center = pos
            self.center_x, self.center_y = self.rect.center

        def animate(self):
            if not self.dead_sprite:
                self.current_sprite += 0.2  #cycles through sprite image list

                if self.current_sprite >= len(self.sprites):
                    self.current_sprite = 0

                self.image = self.sprites[int(self.current_sprite)]

            else:  #displays dead dragon
                self.image = pygame.transform.scale(
                    pygame.image.load('frame-dead.png'), (123, 90))

        def update(self):
            self.animate()

    class Model2(pygame.sprite.Sprite
                 ):  #class for animating and displaying the red dragon sprite

        def __init__(self, pos):
            super().__init__()
            self.sprites = []  #list of frames for animation
            self.sprites.append(
                pygame.transform.scale(pygame.image.load('evil_frame-1.png'),
                                       (123, 90)))
            self.sprites.append(
                pygame.transform.scale(pygame.image.load('evil_frame-2.png'),
                                       (123, 90)))
            self.sprites.append(
                pygame.transform.scale(pygame.image.load('evil_frame-3.png'),
                                       (123, 90)))

            self.current_sprite = 0
            self.image = self.sprites[self.current_sprite]

            self.dead_sprite = False  # boolean for determing if the dragon should be dead or flying
            #RECT
            self.rect = self.image.get_rect()
            self.rect.center = pos
            self.center_x, self.center_y = self.rect.center

        def animate(self):

            if not self.dead_sprite:
                self.current_sprite += 0.2  #cycles through sprite image list

                if self.current_sprite >= len(self.sprites):
                    self.current_sprite = 0

                self.image = self.sprites[int(self.current_sprite)]
            else:  #displays dead dragon
                self.image = pygame.transform.scale(
                    pygame.image.load('evil_dead_dragon.png'), (123, 90))

        def update(self):
            self.animate()

    #BUTTON CLASS INSTANCES (GUI)
    cursor = Cursor("cursor1.png")
    cursor_group = pygame.sprite.Group()
    cursor_group.add(cursor)

    title_button = Button('game_over_text.png', screenx / 2, 70, .3)
    rematch_button = Button('rematch_button.png', screenx / 2, screeny / 2,
                            0.5)
    exit_button = Button('exit_button.png', screenx / 2, (screeny / 2) + 80,
                         .38)
    player1_silver_button = Button('player1_silver_button.png', screenx / 4,
                                   (screeny / 2) + 80, .35)
    player2_silver_button = Button('player2_silver_button.png',
                                   3 * (screenx / 4), (screeny / 2) + 80, .35)
    player1_gold_button = Button('player1_gold_button.png', screenx / 4,
                                 (screeny / 2) + 80, .35)
    player2_gold_button = Button('player2_gold_button.png', 3 * (screenx / 4),
                                 (screeny / 2) + 80, .35)

    #DRAGON MODEL INSTANCES
    model1 = Model1((2 * (screenx / 8), screeny / 2.3))
    model2 = Model2((6 * (screenx / 8), screeny / 2.3))

    model_group = pygame.sprite.Group()
    model_group.add(model1)
    model_group.add(model2)

    running = True
    while running:
        screen.blit(background_surface, (0, 0))

        for event in pygame.event.get():
            if pygame.event == pygame.QUIT:
                running = False
                pygame.quit
                sys.exit()

        if rematch_button.draw():
            play_game()

        if exit_button.draw():
            running = False
            pygame.quit
            sys.exit()

        if p1Win:  #determines how the GUI will look if player1 won the match
            player1_gold_button.draw()
            player2_silver_button.draw()
            model2.dead_sprite = True  #sets the red dragon model to dead

        else:  #determines how the GUI will look if player2 won the match
            player1_silver_button.draw()
            player2_gold_button.draw()
            model1.dead_sprite = True  #sets the green dragon model to dead

        title_button.draw()

        cursor_group.draw(screen)
        cursor_group.update()
        model_group.draw(screen)
        model_group.update()

        pygame.display.flip()

        clock.tick(60)


def play_game():  #PLAYSCREEN

    #SURFACES
    background = pygame.image.load('skyland.png')
    background = pygame.transform.scale(background, (screenx, screeny))

    #VARIABLES
    global charge_value
    charge_value = 1
    global max_charge
    max_charge = 20
    global bullet_speed
    bullet_speed = 8
    global bullet_power
    bullet_power = 5
    global reload_speed
    reload_speed = .3
    global lower_boundary
    lower_boundary = 80

    player_speed = 8

    pygame.mouse.set_visible(False)

    #CLASSES

    class Player1(
            pygame.sprite.Sprite
    ):  #takes care of animating, displaying, and the controlling of the green dragon sprite

        def __init__(self, image_path, pos):
            super().__init__()
            #ANIMATION
            self.sprites = []  #list of frames to animate the dragon flying
            self.sprites.append(
                pygame.transform.scale(pygame.image.load('frame-1.png'),
                                       (82, 60)))
            self.sprites.append(
                pygame.transform.scale(pygame.image.load('frame-2.png'),
                                       (82, 60)))
            self.sprites.append(
                pygame.transform.scale(pygame.image.load('frame-3.png'),
                                       (82, 60)))

            self.firing_sprites = [
            ]  #list of frames to animate the dragon opening its mouth to shoot
            self.firing_sprites.append(
                pygame.transform.scale(pygame.image.load('fire_frame-1.png'),
                                       (82, 60)))
            self.firing_sprites.append(
                pygame.transform.scale(pygame.image.load('fire_frame-2.png'),
                                       (82, 60)))
            self.firing_sprites.append(
                pygame.transform.scale(pygame.image.load('fire_frame-3.png'),
                                       (82, 60)))

            self.current_sprite = 0  #used to cycle through the list of frames for animation
            self.image = self.sprites[self.current_sprite]

            #DEATH ANIMATION
            self.dead_sprite = pygame.transform.scale(
                pygame.image.load('frame-dead.png'), (82, 60))
            self.dead_sprites = []  #list of frames for dead animation
            self.dead_sprites.append(
                pygame.transform.rotate(self.dead_sprite, -30))
            self.dead_sprites.append(
                pygame.transform.rotate(self.dead_sprite, -40))
            self.dead_sprites.append(
                pygame.transform.rotate(self.dead_sprite, -50))
            self.dead_sprites.append(
                pygame.transform.rotate(self.dead_sprite, -60))
            self.dead_sprites.append(
                pygame.transform.rotate(self.dead_sprite, -70))
            self.dead_sprites.append(
                pygame.transform.rotate(self.dead_sprite, -80))
            self.dead_sprites.append(
                pygame.transform.rotate(self.dead_sprite, -90))

            self.current_dead_sprite = 0  #used to cycle through the list of frames for the dead animation
            self.death_done = False

            #RECT
            self.rect = self.image.get_rect()
            self.rect = self.rect.inflate(
                -30, 0)  #resizing rect because image was too big
            self.rect.center = pos
            self.center_x, self.center_y = self.rect.center
            self.center_x -= 30  #adjusts the rect because the image was too big

            #SHOOTING ATTRIBUTES
            self.reloading = True
            self.last_reload_time = time.time()
            self.charge = 0
            self.recoil_value = 0

            #HEALTH
            self.health = 200
            self.dead = False

            #GUI
            self.healthbar = pygame.image.load('health_bar.png')
            self.healthbar = pygame.transform.scale(
                self.healthbar,
                (.75 * self.healthbar.get_width(),
                 .75 * self.healthbar.get_height()))  #scales the image
            self.healthbar_ogx = self.healthbar.get_width()

            self.chargebar = pygame.image.load('energy_bar.png')
            self.chargebar_max = pygame.transform.scale(
                self.chargebar,
                (210, .5 * self.chargebar.get_height()))  # scales the image
            self.chargebar_90 = pygame.transform.scale(
                self.chargebar,
                (189, .5 * self.chargebar.get_height()))  # scales the image
            self.chargebar_80 = pygame.transform.scale(
                self.chargebar,
                (168, .5 * self.chargebar.get_height()))  # scales the image
            self.chargebar_70 = pygame.transform.scale(
                self.chargebar,
                (147, .5 * self.chargebar.get_height()))  # scales the image
            self.chargebar_60 = pygame.transform.scale(
                self.chargebar,
                (126, .5 * self.chargebar.get_height()))  # scales the image
            self.chargebar_50 = pygame.transform.scale(
                self.chargebar,
                (105, .5 * self.chargebar.get_height()))  # scales the image
            self.chargebar_40 = pygame.transform.scale(
                self.chargebar,
                (84, .5 * self.chargebar.get_height()))  # scales the image
            self.chargebar_30 = pygame.transform.scale(
                self.chargebar,
                (63, .5 * self.chargebar.get_height()))  # scales the image
            self.chargebar_20 = pygame.transform.scale(
                self.chargebar,
                (42, .5 * self.chargebar.get_height()))  # scales the image
            self.chargebar_10 = pygame.transform.scale(
                self.chargebar,
                (21, .5 * self.chargebar.get_height()))  # scales the image

        def animate(self):
            self.current_sprite += 0.2  #cycles through sprite image list

            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0  #sets the index counter back to 0 if it gets bigger than the amount of frames in the frame list

            if not self.reloading and pygame.key.get_pressed(
            )[pygame.
              K_SPACE]:  #checks to see if the user is firing to open mouth
                self.image = self.firing_sprites[int(self.current_sprite)]

            elif self.dead:
                self.dead_animation(
                )  #calls the dead animation if the player is dead

            else:
                self.image = self.sprites[int(
                    self.current_sprite
                )]  #sets the sprites image to the current frame of animation

        def dead_animation(self):

            #rotate animation
            if self.current_dead_sprite <= len(self.dead_sprites):
                self.image = self.dead_sprites[int(self.current_dead_sprite)]
                self.current_dead_sprite += 0.4

            delay = 100  #time delay between animation and post game

            #drops the sprite
            if self.rect.centery < screeny + delay:
                self.rect.centery += 6
            else:
                self.death_done = True

        def move(self):
            if pygame.key.get_pressed()[pygame.K_w]:
                if self.rect.top - player_speed >= 0:  #upper boundary
                    self.rect.top -= player_speed  #increments by player_speed
                elif self.rect.top - 1 >= 0:
                    self.rect.top -= 2

            if pygame.key.get_pressed()[pygame.K_s]:
                if self.rect.bottom + player_speed < screeny - lower_boundary:  #lower boundary
                    self.rect.bottom += player_speed
                elif self.rect.bottom + 1 <= screeny - lower_boundary:
                    self.rect.bottom += 2

            if pygame.key.get_pressed()[pygame.K_a]:
                if self.rect.left - player_speed > 0:  #left boundary
                    self.rect.left -= player_speed
                elif self.rect.left - 1 >= 0:
                    self.rect.left -= 2

            if pygame.key.get_pressed()[pygame.K_d]:
                if self.rect.right + player_speed < 200:  #right boundary
                    self.rect.right += player_speed
                elif self.rect.right + 1 < 200:
                    self.rect.right += 2

        def create_bullet(self):
            return Bullet1(self.rect.centerx, self.rect.centery, self.charge)

        def shoot(self):

            if self.reloading and (
                    time.time() - self.last_reload_time
            ) > reload_speed:  #determines when player is done reloading
                self.reloading = False

            if self.reloading == True:
                pass  #print("Reloading..")

            if not self.reloading and self.charge == 0:
                pass  #print("Ready!")

            if pygame.key.get_pressed()[pygame.K_SPACE]:
                if not self.reloading:
                    if self.charge < max_charge:  #sets a cap to the charge
                        self.charge += charge_value  #increases charge

                self.display_chargebar()

            else:
                if not self.reloading:

                    if self.charge > charge_value:  #checks to see if there was a charged shot or single-shot
                        #print("Fire!")
                        bullet_group1.add(self.create_bullet())
                        #self.recoil()
                        self.last_reload_time = time.time()
                        self.reloading = True

                self.charge = 0
                self.display_chargebar()

        def control(self):
            self.move()
            self.shoot()

        def get_hit(self):
            for bullet in bullet_group2:
                if self.rect.colliderect(bullet):
                    explosion_group.add(
                        Explosion(bullet.rect.centerx, bullet.rect.centery))
                    self.health -= bullet.power
                    self.display_healthbar()
                    bullet.kill()

        def display_healthbar(self):

            if self.health > 0:
                self.healthbar = pygame.transform.scale(
                    self.healthbar, ((self.health / 200) * self.healthbar_ogx,
                                     self.healthbar.get_height()))
                screen.blit(self.healthbar, (53, screeny - 35))
            else:
                pass

        def display_chargebar(self):

            if pygame.key.get_pressed()[pygame.K_SPACE]:
                if not self.reloading:
                    if self.charge <= 2:
                        screen.blit(self.chargebar_10,
                                    (42, screeny - 72))  #positions the bar
                    elif self.charge <= 4:
                        screen.blit(self.chargebar_20,
                                    (42, screeny - 72))  #positions the bar
                    elif self.charge <= 6:
                        screen.blit(self.chargebar_30,
                                    (42, screeny - 72))  #positions the bar
                    elif self.charge <= 8:
                        screen.blit(self.chargebar_40,
                                    (42, screeny - 72))  #positions the bar
                    elif self.charge <= 10:
                        screen.blit(self.chargebar_50,
                                    (42, screeny - 72))  #positions the bar
                    elif self.charge <= 12:
                        screen.blit(self.chargebar_60,
                                    (42, screeny - 72))  #positions the bar

                    elif self.charge <= 14:
                        screen.blit(self.chargebar_70,
                                    (42, screeny - 72))  #positions the bar

                    elif self.charge <= 16:
                        screen.blit(self.chargebar_80,
                                    (42, screeny - 72))  #positions the bar

                    elif self.charge <= 18:
                        screen.blit(self.chargebar_90,
                                    (42, screeny - 72))  #positions the bar

                    elif self.charge <= 20:
                        screen.blit(self.chargebar_max,
                                    (42, screeny - 72))  #positions the bar

        def decide_dead(self):
            if self.health <= 0:
                self.dead = True

        def update(self):
            self.display_healthbar()
            self.animate()
            self.get_hit()
            self.decide_dead()
            if not self.dead:
                self.control()

    class Player2(
            pygame.sprite.Sprite
    ):  #takes care of animating, displaying, and the controlling of the green dragon sprite

        def __init__(self, image_path, pos):
            super().__init__()
            self.sprites = []
            self.sprites.append(
                pygame.transform.scale(pygame.image.load('evil_frame-1.png'),
                                       (82, 60)))
            self.sprites.append(
                pygame.transform.scale(pygame.image.load('evil_frame-2.png'),
                                       (82, 60)))
            self.sprites.append(
                pygame.transform.scale(pygame.image.load('evil_frame-3.png'),
                                       (82, 60)))

            self.firing_sprites = []
            self.firing_sprites.append(
                pygame.transform.scale(
                    pygame.image.load('evil_fire_frame-1.png'), (82, 60)))
            self.firing_sprites.append(
                pygame.transform.scale(
                    pygame.image.load('evil_fire_frame-2.png'), (82, 60)))
            self.firing_sprites.append(
                pygame.transform.scale(
                    pygame.image.load('evil_fire_frame-3.png'), (82, 60)))

            self.current_sprite = 0
            self.image = self.sprites[self.current_sprite]

            #DEATH ANIMATION
            self.dead_sprite = pygame.transform.scale(
                pygame.image.load('evil_dead_dragon.png'), (82, 60))
            self.dead_sprites = []  #prepares for rotate animation
            self.dead_sprites.append(
                pygame.transform.rotate(self.dead_sprite, 30))
            self.dead_sprites.append(
                pygame.transform.rotate(self.dead_sprite, 40))
            self.dead_sprites.append(
                pygame.transform.rotate(self.dead_sprite, 50))
            self.dead_sprites.append(
                pygame.transform.rotate(self.dead_sprite, 60))
            self.dead_sprites.append(
                pygame.transform.rotate(self.dead_sprite, 70))
            self.dead_sprites.append(
                pygame.transform.rotate(self.dead_sprite, 80))
            self.dead_sprites.append(
                pygame.transform.rotate(self.dead_sprite, 90))

            self.current_dead_sprite = 0
            self.death_done = False
            #RECT
            self.rect = self.image.get_rect()
            self.rect.center = pos
            self.center_x, self.center_y = self.rect.center

            #SHOOTING ATTRIBUTES
            self.reloading = True
            self.last_reload_time = time.time()
            self.charge = 0
            #HEALTH:
            self.health = 200
            self.dead = False

            #GUI
            self.healthbar = pygame.image.load('health_bar.png')
            self.healthbar = pygame.transform.scale(
                self.healthbar, (.75 * self.healthbar.get_width(),
                                 .75 * self.healthbar.get_height()))
            self.healthbar_og_width = self.healthbar.get_width()

            self.chargebar = pygame.image.load('energy_bar.png')
            self.chargebar_max = pygame.transform.scale(
                self.chargebar,
                (210, .5 * self.chargebar.get_height()))  # scales the image
            self.chargebar_90 = pygame.transform.scale(
                self.chargebar,
                (189, .5 * self.chargebar.get_height()))  # scales the image
            self.chargebar_80 = pygame.transform.scale(
                self.chargebar,
                (168, .5 * self.chargebar.get_height()))  # scales the image
            self.chargebar_70 = pygame.transform.scale(
                self.chargebar,
                (147, .5 * self.chargebar.get_height()))  # scales the image
            self.chargebar_60 = pygame.transform.scale(
                self.chargebar,
                (126, .5 * self.chargebar.get_height()))  # scales the image
            self.chargebar_50 = pygame.transform.scale(
                self.chargebar,
                (105, .5 * self.chargebar.get_height()))  # scales the image
            self.chargebar_40 = pygame.transform.scale(
                self.chargebar,
                (84, .5 * self.chargebar.get_height()))  # scales the image
            self.chargebar_30 = pygame.transform.scale(
                self.chargebar,
                (63, .5 * self.chargebar.get_height()))  # scales the image
            self.chargebar_20 = pygame.transform.scale(
                self.chargebar,
                (42, .5 * self.chargebar.get_height()))  # scales the image
            self.chargebar_10 = pygame.transform.scale(
                self.chargebar,
                (21, .5 * self.chargebar.get_height()))  # scales the image

        def animate(self):
            self.current_sprite += 0.2  #cycles through sprite image list

            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0

            if not self.reloading and pygame.mouse.get_pressed(
            )[0]:  #checks to see if the user is firing to open mouth
                self.image = self.firing_sprites[int(self.current_sprite)]

            elif self.dead:
                self.dead_animation()

            else:
                self.image = self.sprites[int(self.current_sprite)]

        def dead_animation(self):

            #rotate animation
            if self.current_dead_sprite <= len(self.sprites):
                self.image = self.dead_sprites[int(self.current_dead_sprite)]
                self.current_dead_sprite += 0.4

            delay = 100  #time delay between animation and post game

            #drops the sprite
            if self.rect.centery < screeny + delay:
                self.rect.centery += 6
            else:
                self.death_done = True

        def move(self):
            if pygame.key.get_pressed()[pygame.K_UP]:
                if self.rect.top - player_speed >= 0:  #upper boundary
                    self.rect.top -= player_speed  #increments by player_speed
                elif self.rect.top - 1 >= 0:
                    self.rect.top -= 2

            if pygame.key.get_pressed()[pygame.K_DOWN]:
                if self.rect.bottom + player_speed < screeny - lower_boundary:  #lower boundary
                    self.rect.bottom += player_speed
                elif self.rect.bottom + 1 <= screeny - lower_boundary:
                    self.rect.bottom += 2

            if pygame.key.get_pressed()[pygame.K_LEFT]:
                if self.rect.left - player_speed > screenx - 200:  #left boundary
                    self.rect.left -= player_speed
                elif self.rect.left - 1 >= screenx - 200:
                    self.rect.left -= 2

            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                if self.rect.right + player_speed < screenx:  #right boundary
                    self.rect.right += player_speed
                elif self.rect.right + 1 < screenx:
                    self.rect.right += 2

        def create_bullet(self):
            return Bullet2(self.rect.centerx, self.rect.centery, self.charge)

        def shoot(self):
            if self.reloading and (
                    time.time() - self.last_reload_time
            ) > reload_speed:  #determines when player is done reloading
                self.reloading = False

            #if self.reloading == True:
            #print("Reloading..")

            #if not self.reloading and self.charge==0:
            #print("Ready!")

            if pygame.mouse.get_pressed()[0]:
                if not self.reloading:
                    if self.charge < max_charge:
                        self.charge += 1
                        #print("Charging..")
                self.display_chargebar()

            else:
                if not self.reloading:
                    if self.charge >= 0.1:
                        #print("Fire!")
                        bullet_group2.add(self.create_bullet())
                        self.last_reload_time = time.time()
                        self.reloading = True
                self.charge = 0
                self.display_chargebar()

        def control(self):
            self.move()
            self.shoot()

        def get_hit(self):
            for bullet in bullet_group1:
                if self.rect.colliderect(bullet):
                    explosion_group.add(
                        Explosion(bullet.rect.centerx, bullet.rect.centery))
                    self.health -= bullet.power
                    bullet.kill()

        def display_health(self):

            if self.health > 0:
                self.healthbar = pygame.transform.scale(
                    self.healthbar,
                    ((self.health / 200) * self.healthbar_og_width,
                     self.healthbar.get_height()))
                screen.blit(self.healthbar,
                            ((screenx - 50.5) -
                             (self.healthbar_og_width * self.health / 200),
                             screeny - 35))

        def display_chargebar(self):

            if pygame.mouse.get_pressed()[0]:
                if not self.reloading:
                    if self.charge <= 2:
                        screen.blit(
                            self.chargebar_10,
                            (screenx - 62, screeny - 72))  #positions the bar
                    elif self.charge <= 4:
                        screen.blit(
                            self.chargebar_20,
                            (screenx - 62 - self.chargebar_10.get_width(),
                             screeny - 72))  #positions the bar
                    elif self.charge <= 6:
                        screen.blit(
                            self.chargebar_30,
                            (screenx - 62 - self.chargebar_20.get_width(),
                             screeny - 72))  #positions the bar
                    elif self.charge <= 8:
                        screen.blit(
                            self.chargebar_40,
                            (screenx - 62 - self.chargebar_30.get_width(),
                             screeny - 72))  #positions the bar
                    elif self.charge <= 10:
                        screen.blit(
                            self.chargebar_50,
                            (screenx - 62 - self.chargebar_40.get_width(),
                             screeny - 72))  #positions the bar
                    elif self.charge <= 12:
                        screen.blit(
                            self.chargebar_60,
                            (screenx - 62 - self.chargebar_50.get_width(),
                             screeny - 72))  #positions the bar

                    elif self.charge <= 14:
                        screen.blit(
                            self.chargebar_70,
                            (screenx - 62 - self.chargebar_60.get_width(),
                             screeny - 72))  #positions the bar

                    elif self.charge <= 16:
                        screen.blit(
                            self.chargebar_80,
                            (screenx - 62 - self.chargebar_70.get_width(),
                             screeny - 72))  #positions the bar

                    elif self.charge <= 18:
                        screen.blit(
                            self.chargebar_90,
                            (screenx - 62 - self.chargebar_80.get_width(),
                             screeny - 72))  #positions the bar

                    elif self.charge <= 20:
                        screen.blit(
                            self.chargebar_max,
                            (screenx - 62 - self.chargebar_90.get_width(),
                             screeny - 72))  #positions the bar

        def decide_dead(self):
            if self.health <= 0:
                self.dead = True

        def update(self):
            self.animate()
            self.get_hit()
            self.display_health()
            self.decide_dead()
            if not self.dead:
                self.control()

    class Bullet1(pygame.sprite.Sprite):

        def __init__(self, pos_x, pos_y, charge):
            super().__init__()
            self.image = pygame.image.load("fire_ball.png")
            self.image = pygame.transform.scale(self.image, (60, 40))

            self.rect = self.image.get_rect(center=(pos_x, pos_y))
            self.charge = charge
            self.power = charge + bullet_power

        def update(self):
            self.rect.x += bullet_speed + (self.charge)

            if self.rect.x >= screenx:
                self.kill()

    class Bullet2(pygame.sprite.Sprite):

        def __init__(self, pos_x, pos_y, charge):
            super().__init__()
            self.image = pygame.image.load("evil_fire_ball.png")
            self.image = pygame.transform.scale(self.image, (115, 75))
            self.rect = self.image.get_rect(center=(pos_x, pos_y))
            self.charge = charge
            self.power = charge + bullet_power

        def update(self):
            self.rect.x -= bullet_speed + (self.charge)

            for bullet in bullet_group1:
                if bullet.rect.colliderect(self.rect):
                    if self.charge > bullet.charge:  #decides which bullet to destroy based on their charge
                        explosion_group.add(
                            Explosion(bullet.rect.centerx,
                                      bullet.rect.centery))
                        bullet.kill()

                    elif bullet.charge > self.charge:  #decides which bullet to destroy based on their charge
                        explosion_group.add(
                            Explosion(bullet.rect.centerx,
                                      bullet.rect.centery))
                        self.kill()

                    elif bullet.charge == self.charge:  #destroys both if they are same charge
                        explosion_group.add(
                            Explosion(bullet.rect.centerx,
                                      bullet.rect.centery))
                        self.kill()

            if self.rect.x <= 0:  #destroys the bullet after it goes offscreen
                self.kill()

    class Explosion(pygame.sprite.Sprite):

        def __init__(self, pos_x, pos_y):
            super().__init__()
            self.image = pygame.transform.scale(
                pygame.image.load("exp_frame-1.png"), (30, 30))
            self.rect = self.image.get_rect(center=(pos_x, pos_y))

            self.animation_list = []
            self.animation_list.append(
                pygame.transform.scale(pygame.image.load('exp_frame-1.png'),
                                       (40, 40)))
            self.animation_list.append(
                pygame.transform.scale(pygame.image.load('exp_frame-2.png'),
                                       (45, 45)))
            self.animation_list.append(
                pygame.transform.scale(pygame.image.load('exp_frame-3.png'),
                                       (50, 50)))
            self.animation_list.append(
                pygame.transform.scale(pygame.image.load('exp_frame-4.png'),
                                       (55, 55)))
            self.animation_list.append(
                pygame.transform.scale(pygame.image.load('exp_frame-5.png'),
                                       (60, 60)))
            self.animation_list.append(
                pygame.transform.scale(pygame.image.load('exp_frame-6.png'),
                                       (60, 60)))
            self.animation_list.append(
                pygame.transform.scale(pygame.image.load('exp_frame-7.png'),
                                       (60, 60)))
            self.animation_list.append(
                pygame.transform.scale(pygame.image.load('exp_frame-8.png'),
                                       (60, 60)))

            self.current_slide = 0

        def update(self):
            self.current_slide += 0.7

            if self.current_slide < 8:
                self.image = self.animation_list[int(self.current_slide)]
            else:
                self.kill()

    explosion_group = pygame.sprite.Group()

    #player
    player1 = Player1("cat2.png", (screenx / 8, screeny / 2))
    player_group = pygame.sprite.Group()
    player_group.add(player1)

    player2 = Player2("cat2.png", (screenx - (screenx / 8), screeny / 2))
    player_group.add(player2)

    #bullet
    bullet_group1 = pygame.sprite.Group()
    bullet_group2 = pygame.sprite.Group()

    #GUI graphics
    p1_healthbar = Button('p1_empty_healthbar.png', 180, screeny - 30, .75)
    p2_healthbar = Button('p2_empty_healthbar.png', screenx - 180,
                          screeny - 30, .75)

    p1_chargebar = Button('p1_empty_energybar.png', 140, screeny - 70, .55)
    p2_chargebar = Button('p2_empty_energybar.png', screenx - 140,
                          screeny - 70, .55)

    p1_silver_button = Button('player1_silver_button.png', 55, 30, .20)
    p2_silver_button = Button('player2_silver_button.png', screenx - 55, 30,
                              .20)

    title = Button('title.png', screenx / 2, 40, .20)

    GUI_group = pygame.sprite.Group()
    GUI_group.add(p1_healthbar)
    GUI_group.add(p2_healthbar)
    GUI_group.add(p1_chargebar)
    GUI_group.add(p2_chargebar)
    GUI_group.add(p1_silver_button)
    GUI_group.add(p2_silver_button)
    GUI_group.add(title)

    #TITLE AND ICON
    pygame.display.set_caption("Game")
    #icon = pygame.image.load()

    #GAME LOOP
    running = True
    while running:

        for event in pygame.event.get():
            if pygame.event == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

        #Drawing
        screen.blit(background, (0, 0))
        bullet_group1.draw(screen)
        bullet_group2.draw(screen)

        explosion_group.draw(screen)
        GUI_group.draw(screen)
        player_group.draw(screen)

        #Update
        bullet_group1.update()
        bullet_group2.update()
        player_group.update()
        explosion_group.update()
        GUI_group.update()

        pygame.display.flip()

        if player1.death_done:  #checks for player death to end game loop
            running = False
            p1Win = False
            post_game(p1Win)

        elif player2.death_done:
            running = False
            p1Win = True
            post_game(p1Win)

        clock.tick(60)


def main_menu():

    pygame.display.set_caption("Menu")
    background_surface = pygame.image.load('start_background.png')
    background_surface = pygame.transform.scale(background_surface,
                                                (screenx, screeny))
    pygame.mouse.set_visible(False)

    #CLASSES
    class Cursor(pygame.sprite.Sprite):

        def __init__(self, image_path):
            super().__init__()
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.image, (20, 20))
            self.rect = self.image.get_rect(topleft=(screenx / 2, screeny / 2))

        def update(self):

            self.rect.center = pygame.mouse.get_pos()

    class Model1(pygame.sprite.Sprite):

        def __init__(self, pos):
            super().__init__()
            self.sprites = []
            self.sprites.append(
                pygame.transform.scale(pygame.image.load('evil_frame-1.png'),
                                       (123, 90)))
            self.sprites.append(
                pygame.transform.scale(pygame.image.load('evil_frame-2.png'),
                                       (123, 90)))
            self.sprites.append(
                pygame.transform.scale(pygame.image.load('evil_frame-3.png'),
                                       (123, 90)))

            self.current_sprite = 0
            self.image = self.sprites[self.current_sprite]

            #RECT
            self.rect = self.image.get_rect()
            self.rect.center = pos
            self.center_x, self.center_y = self.rect.center

        def animate(self):
            self.current_sprite += 0.2  #cycles through sprite image list

            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0

            self.image = self.sprites[int(self.current_sprite)]

        def update(self):
            self.animate()

    class Model2(pygame.sprite.Sprite):

        def __init__(self, pos):
            super().__init__()
            self.sprites = []
            self.sprites.append(
                pygame.transform.scale(pygame.image.load('frame-1.png'),
                                       (123, 90)))
            self.sprites.append(
                pygame.transform.scale(pygame.image.load('frame-2.png'),
                                       (123, 90)))
            self.sprites.append(
                pygame.transform.scale(pygame.image.load('frame-3.png'),
                                       (123, 90)))

            self.current_sprite = 0
            self.image = self.sprites[self.current_sprite]

            #RECT
            self.rect = self.image.get_rect()
            self.rect.center = pos
            self.center_x, self.center_y = self.rect.center

        def animate(self):
            self.current_sprite += 0.2  #cycles through sprite image list

            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0

            self.image = self.sprites[int(self.current_sprite)]

        def update(self):
            self.animate()

    cursor = Cursor("cursor1.png")
    cursor_group = pygame.sprite.Group()
    cursor_group.add(cursor)

    title_button = Button('title.png', screenx / 2, 70, .3)
    start_button = Button('start_button.png', screenx / 2, screeny / 2, 0.5)
    exit_button = Button('exit_button.png', screenx / 2, (screeny / 2) + 80,
                         .38)
    player1_button = Button('player1_silver_button.png', screenx / 4,
                            (screeny / 2) + 80, .35)
    player2_button = Button('player2_silver_button.png', 3 * (screenx / 4),
                            (screeny / 2) + 80, .35)

    model1 = Model1((6 * (screenx / 8), screeny / 2.3))
    model2 = Model2((2 * (screenx / 8), screeny / 2.3))

    model_group = pygame.sprite.Group()
    model_group.add(model1)
    model_group.add(model2)

    running = True
    while running:
        screen.blit(background_surface, (0, 0))

        for event in pygame.event.get():
            if pygame.event == pygame.QUIT:
                running = False
                pygame.quit
                sys.exit()

        if start_button.draw():
            play_game()

        if exit_button.draw():
            running = False
            pygame.quit
            sys.exit()

        player1_button.draw()
        player2_button.draw()
        title_button.draw()

        cursor_group.draw(screen)
        cursor_group.update()
        model_group.draw(screen)
        model_group.update()

        pygame.display.flip()

        clock.tick(60)


main_menu()
