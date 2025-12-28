import random

class DungeonBase:
    def __init__(self, dungeon_id, seed=None):
        self.dungeon_id = dungeon_id
        self.seed = seed or random.randint(0, 999999)
        
        self.dungeon_map = []
        
        self.width = 10
        self.height = 10
        
    def create_square_room(self):
        for y in range(self.height):
            for x in range(self.width):
                if x == 0 or x == self.height - 1:
                    self.dungeon_map[y][x].set_walkable(False)
                    self.dungeon_map[y][x].set_display_char('#')
                if y == 0 or y == self.width - 1:
                    self.dungeon_map[y][x].set_walkable(False)
                    self.dungeon_map[y][x].set_display_char('#')