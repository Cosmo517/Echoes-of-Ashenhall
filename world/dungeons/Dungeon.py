from world.common.tile import Tile
import random
import os

class Dungeon:
    def __init__(self, width=20, height=20):
        self.dungeon_height = height
        self.dungeon_width = width
        
        # Entrance to the dungeon
        self.entrance_pos_x = 1
        self.entrance_pos_y = 1
        
        # Player Data
        self.player_character = None
        self.player_pos_x = -1
        self.player_pos_y = -1
        
        # Create the dungeon
        self.dungeon_map = [[Tile() for x in range(self.dungeon_width)] for y in range(self.dungeon_height)]
        self.enemies = []
        self.create_square_room()
    
    def create_square_room(self):
        for y in range(self.dungeon_height):
            for x in range(self.dungeon_width):
                if x == 0 or x == self.dungeon_height - 1:
                    self.dungeon_map[y][x].set_walkable(False)
                    self.dungeon_map[y][x].set_display_char('#')
                if y == 0 or y == self.dungeon_width - 1:
                    self.dungeon_map[y][x].set_walkable(False)
                    self.dungeon_map[y][x].set_display_char('#')
    
    def print_dungeon(self):
        for y in range(self.dungeon_height):
            s = ' '
            for x in range(self.dungeon_width):
                s += self.dungeon_map[y][x].get_display_char()
            print(s)
    

    def enter_dungeon(self, player):
        self.player_character = player
        if self.entrance_pos_x is None and self.entrance_pos_y is None:
            while True:
                self.player_pos_x = random.randint(0, self.dungeon_width)
                self.player_pos_y = random.randint(0, self.dungeon_height)
                if self.dungeon_map[self.player_pos_y][self.player_pos_x].get_player_walkable():
                    break
        else:
            self.player_pos_x = self.entrance_pos_x
            self.player_pos_y = self.entrance_pos_y
        self.dungeon_map[self.player_pos_y][self.player_pos_x].set_display_char('@')
        self.dungeon_map[self.player_pos_y][self.player_pos_x].set_entity(self.player_character)
        
    def generate_enemy(self):
        """Handles generating a single enemy (goblin) within the dungeon"""
        while True:
            pos_x = random.randint(1, self.maze_width - 1)
            pos_y = random.randint(1, self.maze_height - 1)
            if not self.dungeon_map[pos_y][pos_x].has_entity() and not self.dungeon_map[pos_y][pos_x].is_wall():
                break
        enemy = Goblin()
        enemy_info = [enemy, pos_x, pos_y]
        self.enemies.append(enemy_info)
        self.dungeon_map[pos_y][pos_x].set_entity(enemy)
        self.dungeon_map[pos_y][pos_x].set_display_char(enemy.get_display_char())
        os.system('cls')
        self.print_map()

    def handle_player_movement(self, key_pressed):
        """Handle the movement of the player when they press a related key"""
        move_dict = {'w': (0, -1), 'a': (-1, 0), 's': (0, 1), 'd': (1, 0)}  # this is in x,y form
        new_x, new_y = 0, 0
        if key_pressed in move_dict:
            move_x, move_y = move_dict[key_pressed]
            new_x, new_y = self.player_pos_x + move_x, self.player_pos_y + move_y

        if (0 <= new_y < self.dungeon_height and 0 <= new_x < self.dungeon_width and
                self.dungeon_map[new_y][new_x].get_player_walkable()):
            user_x, user_y = self.player_pos_x, self.player_pos_y
            self.dungeon_map[user_y][user_x].set_display_char(' ')
            self.dungeon_map[user_y][user_x].set_entity(None)
            self.player_pos_y, self.player_pos_x = new_y, new_x
            self.dungeon_map[new_y][new_x].set_display_char('@')
            self.dungeon_map[new_y][new_x].set_entity(self.player_character)
            os.system('cls')
            self.print_dungeon()
    
    def handle_enemy_movement(self, enemy_info):
        """Handle the enemy movement given a list of enemy info"""
        enemy, pos_x, pos_y = enemy_info[0], enemy_info[1], enemy_info[2]
        move_dict = {'w': (0, -1), 'a': (-1, 0), 's': (0, 1), 'd': (1, 0)}
        attempts = 0
        while True and attempts < 50:
            move_x, move_y = random.choice(list(move_dict.values()))

            new_x = enemy.movement_modifier * move_x + pos_x
            new_y = enemy.movement_modifier * move_y + pos_y
            if not self.dungeon_map[new_y][new_x].has_entity() and not self.dungeon_map[new_y][new_x].is_wall():
                enemy_info[1] = new_x
                enemy_info[2] = new_y
                break
            attempts += 1

        if (0 <= new_y < self.maze_height and 0 <= new_x < self.maze_width and
           not self.dungeon_map[new_y][new_x].is_wall() and self.dungeon_map[new_y][new_x].get_walkable()):
            self.dungeon_map[pos_y][pos_x].set_display_char(' ')
            self.dungeon_map[pos_y][pos_x].set_entity(None)
            self.dungeon_map[new_y][new_x].set_display_char(enemy.get_display_char())
            self.dungeon_map[new_y][new_x].set_entity(enemy)

    def handle_enemy_actions(self):
        """Handle enemy actions, such as movement, attacks"""
        for i in range(len(self.enemies)):
            self.handle_enemy_movement(self.enemies[i])
        os.system('cls')
        self.print_map()
        print(self.enemies)
