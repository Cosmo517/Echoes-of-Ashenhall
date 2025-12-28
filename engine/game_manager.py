import json
import os

STORY_PATH = "story/levels"
SAVE_PATH = "saves"

class GameManager:
    def __init__(self, context):
        self.context = context
        
        self.handle_subscription()
    
    def handle_subscription(self):
        self.context.event_bus.subscribe("dungeon_enter", self.enter_dungeon)
        self.context.event_bus.subscribe("dungeon_exit", self.exit_dungeon)
        self.context.event_bus.subscribe("story_choice", self.story_choice)

    
    def to_dict(self):
        """Converts the GameManager data to a dict"""
        return {
            "current_scene": self.current_scene,
            "current_level": self.current_level,
            "flags": self.flags,
            "inventory": self.inventory,
            "class_type": self.class_type
        }
    
    def start_game(self):
        # for now use this start from beginning
        if self.context.state == "story":
            # lets load intro
            new_state = {"level": 1, "scene": "intro"}
            self.context.event_bus.emit("story_load_scene", {"load_scene": new_state})
    
    @staticmethod
    def from_dict(data):
        """Converts json/dict into a Game Manager"""
        gm = GameManager()
        gm.current_scene = data.get("current_scene", "dungeon_intro")
        gm.current_level = data.get("current_level", "1")
        gm.flags = data.get("flags", {})
        gm.inventory = data.get("inventory", [])
        gm.class_type = data.get("class_type", None)
        return gm
    
    def switch_state(self, new_state):
        self.state = new_state
        self.context.event_bus.emit("state_changed", {"state": new_state})
    
    def enter_dungeon(self, data):
        self.state = "dungeon"
        pass

    def exit_dungeon(self, data):
        self.state = "story"
        pass
    
    def story_choice(self, data):
        pass
    

def load_scene(scene_id):
    """Load a scene JSON file."""
    path = os.path.join(STORY_PATH, f"{scene_id}.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_game(state):
    os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)
    with open(SAVE_PATH, "w", encoding="utf-8") as f:
        json.dump(state.to_dict(), f, indent=2)
        
def load_game():
    if not os.path.exists(SAVE_PATH):
        return GameManager()
    with open(SAVE_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
        return GameManager.from_dict(data)