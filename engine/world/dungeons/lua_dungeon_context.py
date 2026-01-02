import random

# TODO: need to add more APIs
# TODO: work on getting some existing "idea" APIs working

# This is the API Lua is allowed to interact with
class LuaDungeonContext:
    def __init__(self, dungeon, mod_manager):
        self.dungeon = dungeon
        self.mod_manager = mod_manager

    # ---------- TILE OPERATIONS ----------

    def set_tile(self, x, y, char, walkable):
        tile = self.dungeon.get_tile(x, y)
        tile.set_display_char(char)
        tile.set_walkable(walkable)

    def fill(self, char, walkable):
        for y in range(self.dungeon.height):
            for x in range(self.dungeon.width):
                self.set_tile(x, y, char, walkable)

    def carve_room(self, x, y, w, h):
        for iy in range(y, y + h):
            for ix in range(x, x + w):
                if self.dungeon.in_bounds(ix, iy):
                    self.set_tile(ix, iy, ".", True)

    def create_square_room(self, height, width):
        for y in range(height):
            for x in range(width):
                if x == 0 or x == width - 1 or y == 0 or y == height - 1:
                    self.dungeon.get_tile(x, y).set_wall()


    # ---------- EXITS ----------

    def place_exit(self, x, y):
        tile = self.dungeon.get_tile(x, y)
        tile.set_display_char("$")
        tile.set_walkable(True)
        self.dungeon.exit_position = (x, y)

    # ---------- MOBS ----------

    def spawn_mob(self, mob_id, x, y):
        mob_def = self.mod_manager.get_mob_definition(mob_id)
        mob = mob_def.instantiate(x, y)
        self.dungeon.add_entity(mob)

    # ---------- RNG ----------

    def random(self, min_val, max_val):
        return random.randint(min_val, max_val)
