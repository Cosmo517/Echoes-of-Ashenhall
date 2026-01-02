from engine.world.dungeons.default_dungeon import DefaultDungeonGenerator
from engine.world.dungeons.lua_dungeon_generator import LuaDungeonGenerator
from engine.world.dungeons.dungeon_definition import DungeonDefinition
import os
import json

class DungeonManager:
    def __init__(self, context):
        self.context = context
        self.lua_manager = self.context.lua_manager
        self.current_dungeon = None
        self.dungeons = {}
        self.player_location = {"x": 1, "y": 1}
        self.current_dungeon_def = None
        
        self.load_all_dungeons()
        self.handle_subscriptions()

    def handle_subscriptions(self):
        self.context.event_bus.subscribe("enter_dungeon", self.player_entered)
        self.context.event_bus.subscribe("dungeon_player_movement", self.handle_player_move)
    
    def player_entered(self, data):
        self.context.logging_system.log_info(f"[player_entered] data=[{data}]")
        dungeon_def = self.dungeons[data["dungeon_id"]]
        self.player_location = {"x": 1, "y": 1}
        self.current_dungeon_def = dungeon_def
        mod = self.context.mod_manager.get_mod(dungeon_def.mod_id)
        self.current_dungeon = self.build_dungeon(dungeon_def, mod)
        self.current_dungeon.get_tile(1, 1).set_display_char("@")
        self.current_dungeon.print_dungeon(self.context.event_bus)

        self.context.game_manager.state = "dungeon"
    
    def resolve_movement(self, movement):
        movement_map = {"w": [0, -1], "a": [-1, 0], "s": [0, 1], "d": [1, 0]}
        
        return movement_map.get(movement)
    
    def resolve_dungeon_id(self, dungeon_id):
        if ":" in dungeon_id:
            return dungeon_id
        mod = self.context.mod_manager.get_mod(self.current_dungeon_def.get_mod_id()).id
        return f"{mod}:{dungeon_id}"
    
    def handle_player_move(self, data):
        dx, dy = self.resolve_movement(data["input"])
        cur_x = self.player_location["x"]
        cur_y = self.player_location["y"]
        new_x = cur_x + dx
        new_y = cur_y + dy
        
        self.context.logging_system.log_debug(f"[handle_player_move] dx=[{dx}], dy=[{dy}], cur_x=[{cur_x}], cur_y=[{cur_y}], new_x=[{new_x}], new_y=[{new_y}]")
        
        # TODO: Instead we should compare new_x new_y to the exit location in the dungeon json schema. Simple comparison to $ for now
        # TODO: Clean up the below implementation, probably want to extract to various functions
        if self.current_dungeon.get_tile(new_x, new_y).get_display_char() == "$":
            # need to exit the dungeon and move to next scene
            scene_type = self.current_dungeon_def.get_exit_type()
            if scene_type == "story":
                os.system('cls' if os.name == 'nt' else 'clear')
                next_scene = self.current_dungeon_def.get_exit_scene_or_dungeon()
                new_state = {"scene": next_scene}
                self.context.event_bus.emit("story_load_scene", {"load_scene": new_state})
                self.context.game_manager.state = "story"
                return
            # Dungeon load
            else:
                os.system('cls' if os.name == 'nt' else 'clear')
                dungeon_id = self.resolve_dungeon_id(self.current_dungeon_def.get_exit_scene_or_dungeon())
                self.context.game_manager.state = "dungeon"
                self.context.event_bus.emit("enter_dungeon", {"dungeon_id": dungeon_id})
                return
            
        
        if self.current_dungeon.get_tile(new_x, new_y).is_walkable():
            self.context.logging_system.log_debug(f"[handle_player_move] evaluted to walkable")
            self.current_dungeon.get_tile(cur_x, cur_y).set_display_char(" ")
            self.current_dungeon.get_tile(new_x, new_y).set_display_char("@")
            self.player_location["x"] = cur_x + dx
            self.player_location["y"] = cur_y + dy
        
            os.system('cls' if os.name == 'nt' else 'clear')
            self.current_dungeon.print_dungeon(self.context.event_bus)
        
    
    # TODO: move to mod loader?
    def load_all_dungeons(self):
        for mod in self.context.mod_manager.mods:
            dungeon_root = os.path.join(mod.path, "dungeons")
            if not os.path.exists(dungeon_root):
                continue
            
            for root, _, files in os.walk(dungeon_root):
                for file in files:
                    if not file.endswith(".json"):
                        continue
                    
                    path = os.path.join(root, file)
                    
                    with open(path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    dungeon_id = f"{mod.id}:{data["id"]}"
                    self.dungeons[dungeon_id] = DungeonDefinition(mod.id, data)
        

        self.context.logging_system.log_info(f"All dungeons: [{self.dungeons}]")
    
    def build_dungeon(self, dungeon_def, mod):
        gen_type = dungeon_def.get_generator_type()

        if gen_type == "default":
            generator = DefaultDungeonGenerator()
        elif gen_type == "lua":
            script_path = mod.path / dungeon_def.get_generator_script()
            lua_env = self.lua_manager.load_script(script_path)
            generator = LuaDungeonGenerator(lua_env, self.context.mod_manager)
        else:
            raise ValueError(f"Unknown generator type: {gen_type}")

        return generator.generate(dungeon_def, self.context)

    def update(self, delta_time):
        if not self.current_dungeon:
            return

        # TODO: real-time mob AI, projectiles, cooldowns

    def player_exited(self):
        self.current_dungeon = None
        self.context.state = "story"
    