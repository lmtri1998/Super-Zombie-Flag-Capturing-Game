from typing import List
from Grid import Grid, Wall
from Boundary import Boundary, StatBar
from Player import Player, MAX_HP, TempBlock
from Box import WeaponBox, HealthBox
from Label import Timer, Label, TempLabel, Pointer
from Zombie import Zombie
from Map import Map
from Flag import Flag
from Goal import CaptureFlag
import random
import pygame

SCREEN_SIZE = (1200, 700)
FRAME_RATE = 30
SMOOTH_TURNING_FRAME_DELAY = 4
MAIN_MENU = ["mainMenu/frame_0_delay-0.1s.png",
             "mainMenu/frame_1_delay-0.1s.png",
             "mainMenu/frame_2_delay-0.1s.png",
             "mainMenu/frame_3_delay-0.1s.png"]

class Game:
    screen = pygame.display.set_mode(SCREEN_SIZE)
    walls = [Wall([(0, 0), (1, 1), (0, 1)]), Wall([(0, 0), (1, 0), (2, 0), (3, 0)])]

    def __init__(self):
        pygame.init()

    def run_game(self):

        clock = pygame.time.Clock()
        game_state = 2
        while True:
            if game_state == 1:
                game_state = self.start_battle(clock)
            elif game_state == 2:
                game_state = self.menu_screen(clock)
            elif game_state == 0:
                game_state = self.instruction_screen(clock)
            else:
                break

        pygame.quit()


    def menu_screen(self, clock):
        pygame.display.set_caption("Super Zombie Flag Capturing Game")

        # ENTITIES
        # Background
        i = 0
        # Sprites
        # Sprites
        label_color = (255, 255, 255)
        new_game = Label(44, (800, 130))
        new_game.set_color(label_color)
        new_game.set_msg("Start New Game")
        instruction_label = Label(44, (800, 200))
        instruction_label.set_color(label_color)
        instruction_label.set_msg("Instructions")
        quit_label = Label(44, (800, 270))
        quit_label.set_color(label_color)
        quit_label.set_msg("Quit")

        note = Label(20, (925, 675))
        note.set_color(label_color)
        note.set_msg("Micheal Lin , Bill Le , Ian Chen")


        pointer = Pointer(44, [(750, 130), (750, 200), (750, 270)], [1, 0, 3])
        pointer.set_color(label_color)
        pointer.set_msg("*")
        sprite = pygame.sprite.OrderedUpdates(pointer)
        keep_going = True

        # LOOP
        while keep_going:
            i = (i + 1) % 4
            # TIME
            clock.tick(FRAME_RATE)
            background = pygame.image.load(MAIN_MENU[i])
            background = pygame.transform.scale(background, (1200, 700))
            self.screen.blit(background, (0, 0))
            self.screen.blit(new_game.image, new_game)
            self.screen.blit(instruction_label.image, instruction_label)
            self.screen.blit(quit_label.image, quit_label)
            self.screen.blit(note.image, note)

            # EVENT HANDLING

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 3
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        pointer.move_next()
                    elif event.key == pygame.K_UP:
                        pointer.move_previous()
                    if event.key == pygame.K_RETURN:
                        return pointer.get_value()

            if pygame.key.get_pressed()[pygame.K_c]:
                return 1

            sprite.clear(self.screen, background)
            sprite.update()
            sprite.draw(self.screen)
            pygame.display.flip()

    def instruction_screen(self, clock):
        pygame.display.set_caption("Instructions!!")

        # ENTITIES
        # Background
        background = pygame.Surface(self.screen.get_size())
        background.fill((0, 0, 0))
        self.screen.blit(background, (0, 0))

        label_color = (255, 255, 255)
        line_1 = Label(30, (200, 70))
        line_1.set_color(label_color)
        line_1.set_msg("Your goal each round is to deliver the flag to the enemy base while")
        line_2 = Label(30, (100, 110))
        line_2.set_color(label_color)
        line_2.set_msg(" fighting off your opponent and zombies* The game will be in a Best of 3 format* ")
        line_3 = Label(30, (100, 150))
        line_3.set_color(label_color)
        line_3.set_msg("where player needs to win at least two rounds to win overall* Player 1 will")
        line_4 = Label(30, (100, 190))
        line_4.set_color(label_color)
        line_4.set_msg("  move using the directional key and attack with the right control key* Player 2 ")
        line_5 = Label(30, (100, 230))
        line_5.set_color(label_color)
        line_5.set_msg("will move using the AWSD buttons and attack with the Spacebar*")
        line_6 = Label(30, (200, 270))
        line_6.set_color(label_color)
        line_6.set_msg("Please press Enter to continue*")

        labels = [line_1, line_2, line_3, line_4, line_5, line_6]



        keep_going = True
        i = 0
        # LOOP
        while keep_going:
            i = (i + 1) % 4
            # TIME
            clock.tick(FRAME_RATE)
            background = pygame.image.load(MAIN_MENU[i])
            background = pygame.transform.scale(background, (1200, 700))
            self.screen.blit(background, (0, 0))
            for l in labels:
                l.set_color(label_color)
                self.screen.blit(l.image, l)

            # TIME
            clock.tick(FRAME_RATE)

            # EVENT HANDLING

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 3
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return 2


            pygame.display.flip()

    def start_battle(self, clock):
        pygame.display.set_caption("Fight!!")

        # ENTITIES
        # Background
        background = pygame.Surface(self.screen.get_size())
        background.fill((0, 0, 0))
        self.screen.blit(background, (0, 0))
        # Sprites
        top_widget_size = (self.screen.get_size()[0], round(self.screen.get_size()[1]/10))
        top_widget = Boundary((self.screen.get_size()[0]/2,
                           round(self.screen.get_size()[1]/20)), color=(255, 255, 0), size=top_widget_size)
        # Grids
        grid_sprites, safe_grid, grid_position = self.make_grid((0, round(self.screen.get_size()[1]/10)))
        curr_map = Map(grid_position)
        obsticles = curr_map.make_map()
        potential_box = curr_map.get_box_position()
        obsticles = pygame.sprite.Group(obsticles)


        # Boundary
        top_boundary = Boundary((600, 69), (255, 255, 255), (1200, 20))
        left_boundary = Boundary((-4, 350), (255, 255, 255), (20, 700))
        right_boundary = Boundary((1204, 350), (255, 255, 255), (20, 700))
        bottom_boundary = Boundary((600, 701), (255, 255, 255), (1200, 20))
        top_boundary.make_invisible()
        left_boundary.make_invisible()
        right_boundary.make_invisible()
        bottom_boundary.make_invisible()
        obsticles.add(top_boundary, left_boundary, right_boundary, bottom_boundary)

        # Player
        player_1 = Player(grid_position[7][32])
        player_2 = Player(grid_position[7][0])
        player_1_attacks = pygame.sprite.Group()
        player_2_attacks = pygame.sprite.Group()

        # Player score zone
        p1_score_zone = Boundary((0, 0), (0, 0, 0), (72, 144))
        p1_score_zone.rect.topleft = (grid_position[6][0][0] - 18, grid_position[6][0][1] - 18)
        p1_score_zone.make_invisible()
        p2_score_zone = Boundary((0, 0), (0, 0, 0), (72, 144))
        p2_score_zone.rect.topleft = (grid_position[6][31][0] - 18, grid_position[6][31][1] - 18)
        p2_score_zone.make_invisible()
        score_zone = [p1_score_zone, p2_score_zone]

        # Zombies
        zombie_group = pygame.sprite.Group()
        zombie_group.add(Zombie(player_1, player_2, (500, -5), safe_grid))
        zombie_group.add(Zombie(player_1, player_2, (700, -5), safe_grid))
        zombie_group.add(Zombie(player_1, player_2, (600, 350), safe_grid))
        zombie_group.add(Zombie(player_1, player_2, (500, 705), safe_grid))
        zombie_group.add(Zombie(player_1, player_2, (700, 705), safe_grid))

        # HP Bar
        player_2_bar = StatBar((200, 35), (0, 255, 0), (300, 25), MAX_HP)
        player_1_bar = StatBar((1000, 35), (0, 255, 0), (300, 25), MAX_HP)
        player_1_bar.set_reversed_direction()
        bars = [player_2_bar.get_full_bar((255, 0, 0)), player_1_bar.get_full_bar((255, 0, 0))]

        # Box

        # Item Box
        box_sprites = pygame.sprite.Group()

        # Goals
        flag = Flag((600, 350))
        goal = CaptureFlag([player_1, player_2], score_zone, flag, num_round=3)
        # Label color
        p1_label_color = (0, 0, 255)
        p2_label_color = (255, 0, 0)
        # Flag
        flag_p2 = Label(44, (400, 35))
        flag_p2.set_color(p2_label_color)
        flag_p1 = Label(44, (780, 35))
        flag_p1.set_color(p1_label_color)


        # timer
        timer = Timer(30, (560, 35), 4, 20, FRAME_RATE)
        # Labels
        p2_label = Label(20,(20, 35))
        p2_label.set_color(p2_label_color)
        p2_label.set_msg("P2  ")
        p1_label = Label(20, (1160, 35))
        p1_label.set_color(p1_label_color)
        p1_label.set_msg("P1")

        p1_head = Label(15, (player_1.rect.centerx-8, player_1.rect.top - 5))
        p1_head.set_color(p1_label_color)
        p1_head.set_msg("P1")
        p2_head = Label(15, (player_2.rect.centerx-8, player_2.rect.top - 5))
        p2_head.set_color(p2_label_color)
        p2_head.set_msg("P2")

        p1_weapon = Label(20, (990, 56))
        p1_weapon.set_msg("sada")
        p2_weapon = Label(20, (170, 56))
        p2_weapon.set_msg("sada")

        labels = [p1_label, p2_label, p1_head, p2_head, p1_weapon, p2_weapon, flag_p1, flag_p2]

        keep_going = True
        box_flag = True
        all_sprites = pygame.sprite.OrderedUpdates(grid_sprites, obsticles, flag, player_1, player_2, zombie_group,
                                                   top_widget, timer, labels, bars, player_1_bar, player_2_bar)
        # LOOP
        while keep_going:
            if goal.screen_pause:
                pygame.time.wait(1500)
                goal.screen_pause = False
            # TIME
            clock.tick(FRAME_RATE)

            if timer.get_real_second() % 5 == 0:
                # Box
                if box_flag:
                    box_flag = False
                    box = self.generate_box(potential_box)
                    box_sprites.add(box)
                    all_sprites.add(box)
            else:
                box_flag = True

            if timer.get_real_second() % 20 == 0 and len(zombie_group) <= 1:
                zombie_group.add(Zombie(player_1, player_2, (500, -5), safe_grid))
                zombie_group.add(Zombie(player_1, player_2, (700, -5), safe_grid))
                zombie_group.add(Zombie(player_1, player_2, (600, 350), safe_grid))
                zombie_group.add(Zombie(player_1, player_2, (500, 705), safe_grid))
                zombie_group.add(Zombie(player_1, player_2, (700, 705), safe_grid))
                all_sprites.add(zombie_group)


            for z in zombie_group:
                z.move(zombie_group)

            # Check for Goal
            if goal.check_for_win():
                keep_going = False
            if timer.time_up():
                keep_going = False

            flag_p1.set_msg(str(goal.score[0]))
            flag_p2.set_msg(str(goal.score[1]))
            # EVENT HANDLING
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 3
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        keep_going = False

            #Player 1 event handle
            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                temp_block = TempBlock(player_1.rect.center, player_1.rect.size)
                temp_block.rect.x += player_1.velocity
                if pygame.sprite.spritecollide(temp_block, obsticles, False):
                    # Check the previous directoin
                    if player_1.direction == 1 or player_1.prev_direction == 1:
                        i = 1
                        # Check if the we continue with previous direction for more frames will be able to pass through
                        while i < player_1.velocity * SMOOTH_TURNING_FRAME_DELAY:
                            i += 1
                            temp_block.rect.y += 1
                            if not pygame.sprite.spritecollide(temp_block, obsticles, False):
                                player_1.go_down()
                                break
                    elif player_1.direction == 3 or player_1.prev_direction == 3:
                        i = 1
                        while i < player_1.velocity * SMOOTH_TURNING_FRAME_DELAY:
                            i += 1
                            temp_block.rect.y -= 1
                            if not pygame.sprite.spritecollide(temp_block, obsticles, False):
                                player_1.go_up()
                                break
                    else:
                        pass
                else:
                    player_1.go_right()

            elif pygame.key.get_pressed()[pygame.K_DOWN]:
                temp_block = TempBlock(player_1.rect.center, player_1.rect.size)
                temp_block.rect.y += player_1.velocity
                if pygame.sprite.spritecollide(temp_block, obsticles, False):
                    if player_1.direction == 0 or player_1.prev_direction == 0:
                        i = 1
                        while i < player_1.velocity * SMOOTH_TURNING_FRAME_DELAY:
                            i += 1
                            temp_block.rect.x += 1
                            if not pygame.sprite.spritecollide(temp_block, obsticles, False):
                                player_1.go_right()
                                break
                    elif player_1.direction == 2 or player_1.prev_direction == 2:
                        i = 1
                        while i < player_1.velocity * SMOOTH_TURNING_FRAME_DELAY:
                            i += 1
                            temp_block.rect.x -= 1
                            if not pygame.sprite.spritecollide(temp_block, obsticles, False):
                                player_1.go_left()
                                break
                    else:
                        pass
                else:
                    player_1.go_down()

            elif pygame.key.get_pressed()[pygame.K_UP]:
                temp_block = TempBlock(player_1.rect.center, player_1.rect.size)
                temp_block.rect.y -= player_1.velocity
                if pygame.sprite.spritecollide(temp_block, obsticles, False):
                    if player_1.direction == 0 or player_1.prev_direction == 0:
                        i = 1
                        while i < player_1.velocity * SMOOTH_TURNING_FRAME_DELAY:
                            i += 1
                            temp_block.rect.x += 1
                            if not pygame.sprite.spritecollide(temp_block, obsticles, False):
                                player_1.go_right()
                                break
                    elif player_1.direction == 2 or player_1.prev_direction == 2:
                        i = 1
                        while i < player_1.velocity * SMOOTH_TURNING_FRAME_DELAY:
                            i += 1
                            temp_block.rect.x -= 1
                            if not pygame.sprite.spritecollide(temp_block, obsticles, False):
                                player_1.go_left()
                                break
                    else:
                        pass
                else:
                    player_1.go_up()


            elif pygame.key.get_pressed()[pygame.K_LEFT]:
                temp_block = TempBlock(player_1.rect.center, player_1.rect.size)
                temp_block.rect.x -= player_1.velocity
                if pygame.sprite.spritecollide(temp_block, obsticles, False):
                    if player_1.direction == 1 or player_1.prev_direction == 1:
                        i = 1
                        while i < player_1.velocity * SMOOTH_TURNING_FRAME_DELAY:
                            i += 1
                            temp_block.rect.y += 1
                            if not pygame.sprite.spritecollide(temp_block, obsticles, False):
                                player_1.go_down()
                                break
                    elif player_1.direction == 3 or player_1.prev_direction == 3:
                        i = 1
                        while i < player_1.velocity * SMOOTH_TURNING_FRAME_DELAY:
                            i += 1
                            temp_block.rect.y -= 1
                            if not pygame.sprite.spritecollide(temp_block, obsticles, False):
                                player_1.go_up()
                                break
                    else:
                        pass
                else:
                    player_1.go_left()

            if pygame.key.get_pressed()[pygame.K_RCTRL]:
                lst = player_1.attack()
                player_1_attacks.add(lst)
                all_sprites.add(lst)
            # Player 2 event handle
            if pygame.key.get_pressed()[pygame.K_d]:
                temp_block = TempBlock(player_2.rect.center, player_2.rect.size)
                temp_block.rect.x += player_2.velocity
                if pygame.sprite.spritecollide(temp_block, obsticles, False):
                    # Check the previous directoin
                    if player_2.direction == 1 or player_2.prev_direction == 1:
                        i = 1
                        # Check if the we continue with previous direction for more frames will be able to pass through
                        while i < player_2.velocity * SMOOTH_TURNING_FRAME_DELAY:
                            i += 1
                            temp_block.rect.y += 1
                            if not pygame.sprite.spritecollide(temp_block, obsticles, False):
                                player_2.go_down()
                                break
                    elif player_2.direction == 3 or player_2.prev_direction == 3:
                        i = 1
                        while i < player_2.velocity * SMOOTH_TURNING_FRAME_DELAY:
                            i += 1
                            temp_block.rect.y -= 1
                            if not pygame.sprite.spritecollide(temp_block, obsticles, False):
                                player_2.go_up()
                                break
                    else:
                        pass
                else:
                    player_2.go_right()

            elif pygame.key.get_pressed()[pygame.K_s]:
                temp_block = TempBlock(player_2.rect.center, player_2.rect.size)
                temp_block.rect.y += player_2.velocity
                if pygame.sprite.spritecollide(temp_block, obsticles, False):
                    if player_2.direction == 0 or player_2.prev_direction == 0:
                        i = 1
                        while i < player_2.velocity * SMOOTH_TURNING_FRAME_DELAY:
                            i += 1
                            temp_block.rect.x += 1
                            if not pygame.sprite.spritecollide(temp_block, obsticles, False):
                                player_2.go_right()
                                break
                    elif player_2.direction == 2 or player_2.prev_direction == 2:
                        i = 1
                        while i < player_2.velocity * SMOOTH_TURNING_FRAME_DELAY:
                            i += 1
                            temp_block.rect.x -= 1
                            if not pygame.sprite.spritecollide(temp_block, obsticles, False):
                                player_2.go_left()
                                break
                    else:
                        pass
                else:
                    player_2.go_down()

            elif pygame.key.get_pressed()[pygame.K_w]:
                temp_block = TempBlock(player_2.rect.center, player_2.rect.size)
                temp_block.rect.y -= player_2.velocity
                if pygame.sprite.spritecollide(temp_block, obsticles, False):
                    if player_2.direction == 0 or player_2.prev_direction == 0:
                        i = 1
                        while i < player_2.velocity * SMOOTH_TURNING_FRAME_DELAY:
                            i += 1
                            temp_block.rect.x += 1
                            if not pygame.sprite.spritecollide(temp_block, obsticles, False):
                                player_2.go_right()
                                break
                    elif player_2.direction == 2 or player_2.prev_direction == 2:
                        i = 1
                        while i < player_2.velocity * SMOOTH_TURNING_FRAME_DELAY:
                            i += 1
                            temp_block.rect.x -= 1
                            if not pygame.sprite.spritecollide(temp_block, obsticles, False):
                                player_2.go_left()
                                break
                    else:
                        pass
                else:
                    player_2.go_up()

            elif pygame.key.get_pressed()[pygame.K_a]:
                temp_block = TempBlock(player_2.rect.center, player_2.rect.size)
                temp_block.rect.x -= player_2.velocity
                if pygame.sprite.spritecollide(temp_block, obsticles, False):
                    if player_2.direction == 1 or player_2.prev_direction == 1:
                        i = 1
                        while i < player_2.velocity * SMOOTH_TURNING_FRAME_DELAY:
                            i += 1
                            temp_block.rect.y += 1
                            if not pygame.sprite.spritecollide(temp_block, obsticles, False):
                                player_2.go_down()
                                break
                    elif player_2.direction == 3 or player_2.prev_direction == 3:
                        i = 1
                        while i < player_2.velocity * SMOOTH_TURNING_FRAME_DELAY:
                            i += 1
                            temp_block.rect.y -= 1
                            if not pygame.sprite.spritecollide(temp_block, obsticles, False):
                                player_2.go_up()
                                break
                    else:
                        pass
                else:
                    player_2.go_left()

            if pygame.key.get_pressed()[pygame.K_SPACE]:
                lst2 = player_2.attack()
                player_2_attacks.add(lst2)
                all_sprites.add(lst2)

            # Collisions handleling
            for box1 in pygame.sprite.spritecollide(player_1, box_sprites, False):
                temp_label = TempLabel(15, (player_1.rect.centerx-8, player_1.rect.top - 5), 3, FRAME_RATE)
                temp_label.set_msg(box1.__str__())
                all_sprites.add(temp_label)
                box1.collide(player_1)
            for box2 in pygame.sprite.spritecollide(player_2, box_sprites, False):
                box2.collide(player_2)
                temp_label = TempLabel(15, (player_2.rect.centerx - 8, player_2.rect.top - 5), 3, FRAME_RATE)
                temp_label.set_msg(box2.__str__())
                all_sprites.add(temp_label)


            # Zombie hit player
            for zombie in pygame.sprite.spritecollide(player_1, zombie_group, False):
                zombie.collide(player_1)
            for zombie in pygame.sprite.spritecollide(player_2, zombie_group, False):
                zombie.collide(player_2)

            # Players hit zombies
            for zombie in zombie_group:
                for bullet in pygame.sprite.spritecollide(zombie, player_2_attacks, False):
                    bullet.collide(zombie)
                for bullet in pygame.sprite.spritecollide(zombie, player_1_attacks, False):
                    bullet.collide(zombie)

            # bullet_hit_walls
            for wall in obsticles:
                for bullet in pygame.sprite.spritecollide(wall, player_1_attacks, False):
                    bullet.end()
                for bullet in pygame.sprite.spritecollide(wall, player_2_attacks, False):
                    bullet.end()
            # Player_1 attacks
            for hit in pygame.sprite.spritecollide(player_2, player_1_attacks, False):
                hit.collide(player_2)

            # Player_2 attacks
            for hit in pygame.sprite.spritecollide(player_1, player_2_attacks, False):
                hit.collide(player_1)

            # Player hp bar
            player_2_bar.set_curr_stat(player_2.health)
            player_1_bar.set_curr_stat(player_1.health)

            # Player head
            p1_head.set_position((player_1.rect.centerx-8, player_1.rect.top - 5))
            p2_head.set_position((player_2.rect.centerx-8, player_2.rect.top - 5))

            p1_weapon.set_msg(str(player_1.weapon))
            p2_weapon.set_msg(str(player_2.weapon))

            if player_1.is_dead():
                if flag.get_player() == player_1:
                    flag.drop()
                player_1.respawn()

            if player_2.is_dead():
                if flag.get_player() == player_2:
                    flag.drop()
                player_2.respawn()
            for zombie in zombie_group:
                if zombie.is_dead(): zombie.kill()


            all_sprites.clear(self.screen, background)
            all_sprites.update()
            all_sprites.draw(self.screen)
            pygame.display.flip()

            lst = player_1.weapon.update()
            player_1_attacks.add(lst)
            all_sprites.add(lst)

            lst = player_2.weapon.update()
            player_2_attacks.add(lst)
            all_sprites.add(lst)

        end_msg = Label(60, (500, 350))
        end_msg.set_color((255, 255, 0))
        end_msg.set_msg(goal.get_wining_msg())
        self.screen.blit(end_msg.image, end_msg)
        pygame.display.flip()
        pygame.time.wait(2000)
        return 2

    def make_grid(self, init_position):

        grid_group = []
        grid_position = []
        safe_grid = []
        grid_size = (36, 36)
        grid_x = round(init_position[0] + grid_size[0]/2)+6
        grid_y = round(init_position[1] + grid_size[1]/2)+9
        for row in range(17):
            grid_position.append([])
            for col in range(33):
                if ((0 <= col <= 1) or (31 <= col <= 32)) and (6 <= row <= 9):
                    grid = Grid((grid_x, grid_y), (255, 255, 0), grid_size, is_safe_grid=True)
                    safe_grid.append(grid)
                    grid_group.append(grid)
                else:
                    grid_group.append(Grid((grid_x, grid_y),(0, 255, 0), grid_size))
                grid_position[row].append((grid_x, grid_y))
                grid_x += grid_size[0]
            grid_y += grid_size[1]
            grid_x = round(init_position[0] + grid_size[0]/2) + 6

        return grid_group, safe_grid, grid_position

    def make_map(self, grid_list):
        wall_A = Wall([(0, 0), (1, 0), (2, 0)])
        wall_B = Wall([(0, 0)])
        wall_C = Wall([(0, 0), (0, 1), (0, 2)])
        wall_D = Wall([(0, 0), (0, 1), (1, 0), (1, 1)])
        wall_E = Wall([(0, 0), (0, 1), (1, 1), (1, 2)])
        wall_F = Wall([(1, 0), (1, 1), (0, 1), (0, 2)])
        wall_G = Wall([(0, 0), (1, 0), (1, 1), (2, 1)])
        wall_H = Wall([(0, 1), (1, 1), (1, 0), (2, 0)])

        wall_1 = Wall([(0, 2), (0, 1), (0, 0), (1, 0), (2, 0)])
        wall_2 = Wall([(2, 2), (2, 1), (0, 0), (1, 0), (2, 0)])
        wall_3 = Wall([(0, 2), (0, 1), (0, 0), (1, 2), (2, 2)])
        wall_4 = Wall([(2, 2), (2, 1), (0, 2), (1, 2), (2, 0)])

        sprites = []

        sprites.extend(wall_1.get_obsticle(grid_list[3][9], 36))
        sprites.extend(wall_3.get_obsticle(grid_list[10][9], 36))
        sprites.extend(wall_4.get_obsticle(grid_list[10][21], 36))
        sprites.extend(wall_2.get_obsticle(grid_list[3][21], 36))

        sprites.extend(wall_E.get_obsticle(grid_list[7][14], 36))
        sprites.extend(wall_E.get_obsticle(grid_list[6][17], 36))



        return sprites

    def generate_box(self, lst):
        if random.randint(0, 10) < 3:
            box = HealthBox
        else:
            box = WeaponBox
        return box(random.choice(lst))



if __name__ == "__main__":
    game = Game()
    game.run_game()
