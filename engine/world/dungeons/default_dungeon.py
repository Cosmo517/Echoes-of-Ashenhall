from engine.world.dungeons.dungeon_generator import DungeonGenerator
from engine.world.dungeons.dungeon import Dungeon
from engine.world.common.tile import Tile

class DefaultDungeonGenerator(DungeonGenerator):
    def generate(self, dungeon_def, context):
        width, height = dungeon_def.get_size()
        dungeon = Dungeon(dungeon_def, width, height)

        # Fill with floor
        for y in range(height):
            for x in range(width):
                dungeon.set_tile(x, y, Tile())

        # TODO: make a better implementation for room generation
        self.create_square_room(dungeon)
        # TODO: place an actual exit
        self.place_exit(dungeon, dungeon_def)
        # TODO: spawn mobs
        # self.spawn_mobs(dungeon, dungeon_def, context)

        return dungeon

    def create_square_room(self, dungeon):
        for y in range(dungeon.height):
            for x in range(dungeon.width):
                if x == 0 or x == dungeon.width - 1 or y == 0 or y == dungeon.height - 1:
                    dungeon.get_tile(x, y).set_wall()

    def place_exit(self, dungeon, dungeon_def):
        exit_def = dungeon_def.get_exit()
        x, y = dungeon.width - 2, dungeon.height - 2
        dungeon.add_exit({"x": x, "y": y, "exit": exit_def})

    def spawn_mobs(self, dungeon, dungeon_def, context):
        for mob_id, count in dungeon_def.get_mobs().items():
            for _ in range(count):
                x, y = context.get_random_floor_tile(dungeon)
                mob = context.spawn_mob(mob_id, x, y)
                dungeon.add_mob(mob)