from engine.world.dungeons.dungeon_generator import DungeonGenerator
from engine.world.dungeons.lua_dungeon_context import LuaDungeonContext


class LuaDungeonGenerator(DungeonGenerator):
    def __init__(self, lua_env, mod_manager):
        self.lua_env = lua_env
        self.mod_manager = mod_manager

    def generate(self, dungeon_def, context):
        width, height = dungeon_def.get_size()

        dungeon = context.create_empty_dungeon(
            dungeon_def,
            width,
            height
        )

        lua_context = LuaDungeonContext(
            dungeon,
            self.mod_manager
        )

        self.lua_env.generate(dungeon, lua_context)

        return dungeon
