class DungeonDefinition:
    def __init__(self, mod_id, dungeon_json: dict):
        self.mod_id = mod_id
        self.id = dungeon_json["id"]
        self.name = dungeon_json["name"]
        self.size = dungeon_json["size"]
        self.mobs = dungeon_json.get("mobs", {})
        self.exit = dungeon_json.get("exit")

        self.generator = dungeon_json.get("generator", {"type": "default"})
        
    def get_id(self):
        return self.id
    
    def get_mod_id(self):
        return self.mod_id
    
    def get_name(self):
        return self.name
    
    def get_size(self):
        return self.size
    
    def get_mobs(self):
        return self.mobs
    
    def get_exit(self):
        return self.exit
    
    def get_exit_type(self):
        return self.exit["type"]
    
    def get_exit_scene_or_dungeon(self):
        if self.get_exit_type() == "story":
            return self.exit["next_scene"]
        else:
            return self.exit["dungeon_id"]
    
    def get_generator(self):
        return self.generator
    
    def get_generator_type(self):
        return self.generator["type"]

    def get_generator_script(self):
        return self.generator.get("script")