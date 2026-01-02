import random

class GameContext:
    def __init__(self):
        self.event_bus = None               # Global event system
        
        self.player = None                  # Player instance
        
        # FIXME: Moved the below to game_manager. might move it back
        # self.inventory = []                 # Players inventory
        
        # self.flags = []                     # Gameplay flags
        
        # self.current_scene = "intro"        # Json File
        # self.current_level = "1"            # Folder
        # self.state = "story"                # Game State (story/dungeon)
        
        self.mod_manager = None              # Loads mods
        self.lua_manager = None              # Handles Lua Code
        self.combat_manager = None           # CombatManager
        self.dungeon_manager = None          # DungeonManager
        self.input_system = None             # InputSystem
        self.render_system = None            # RenderSystem
        self.story_manager = None            # StoryManager
        self.logging_system = None           # LoggingSystem
        self.game_manager = None             # GameManager
    
    # TODO: Currently used by lua_dungeon_generator. Maybe move this..?
    def create_empty_dungeon(self, dungeon_def, width, height):
        from engine.world.dungeons.dungeon import Dungeon
        from engine.world.common.tile import Tile

        dungeon = Dungeon(dungeon_def, width, height)
        for y in range(height):
            for x in range(width):
                dungeon.set_tile(x, y, Tile())
        
        return dungeon

    # TODO: Potentially good function, just should be moved to a proper place I think
    def get_random_floor_tile(self, dungeon):
        # prototype-safe random
        while True:
            x = random.randint(1, dungeon.width - 2)
            y = random.randint(1, dungeon.height - 2)
            if dungeon.get_tile(x, y).walkable:
                return x, y

    def spawn_mob(self, mob_id, x, y):
        # TODO: actually implement the following functions
        mob_def = self.mod_manager.get_mob_definition(mob_id)
        mob = mob_def.instantiate(x, y)
        self.combatManager.register_entity(mob)
        return mob
