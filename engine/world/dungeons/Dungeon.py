class Dungeon:
    def __init__(self, dungeon_def, width, height):
        self.definition = dungeon_def
        self.width = width
        self.height = height
        
        self.tiles = [
            [None for _ in range(width)]
            for _ in range(height)
        ]
        
        self.mobs = []
        self.exits = []
        
    def set_tile(self, x, y, tile):
        self.tiles[y][x] = tile

    def get_tile(self, x, y):
        return self.tiles[y][x]

    def add_mob(self, mob):
        self.mobs.append(mob)

    def add_exit(self, exit_tile):
        x = exit_tile["x"]
        y = exit_tile["y"]
        self.tiles[y][x].set_display_char("$")
        self.exits.append(exit_tile)
    
    def print_dungeon(self, event_bus):
        for y in range(self.height):
            s = ' '
            for x in range(self.width):
                s += self.tiles[y][x].get_display_char()
            event_bus.emit("add_text", {"display_text": s})

