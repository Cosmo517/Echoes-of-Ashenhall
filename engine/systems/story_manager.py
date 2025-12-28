import os
import json
from engine.utils.Scene import Scene

class StoryManager:
    def __init__(self, context, mods):
        self.context = context
        self.mods = mods
        self.current_scene = None
        self.scenes = {}  # scene_id will map to Scene object
        
        self.load_all_scenes()
        self.handle_subscription()
    
    def handle_subscription(self):
        self.context.event_bus.subscribe("story_load_scene", self.handle_load_scene)
        self.context.event_bus.subscribe("ACTION", self.handle_action)
        
    def load_all_scenes(self):
        for mod in self.mods:
            story_root = os.path.join(mod.path, "story")
            if not os.path.exists(story_root):
                continue
            
            for root, _, files in os.walk(story_root):
                for file in files:
                    if not file.endswith(".json"):
                        continue
                    
                    path = os.path.join(root, file)
                    
                    with open(path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    
                    scene_id = f"{mod.id}:{data["scene_id"]}"
                    self.scenes[scene_id] = Scene(data, mod.id)
        self.context.loggingSystem.log_info(f"All scenes: [{self.scenes}]")
        
    def resolve_scene_id(self, next_scene_id):
        if ":" in next_scene_id:
            return next_scene_id
        
        return f"{self.current_scene.mod_id}:{next_scene_id}"
    
    def handle_action(self, choice):
        # Get the choice the user selected
        user_choice_num = int(choice["input"])
        user_choice_adjusted = user_choice_num - 1
        user_choice = self.current_scene.get_choice(user_choice_adjusted)
        self.context.loggingSystem.log_info(f"User selected choice {user_choice_num} which maps to choice {user_choice_adjusted}: {user_choice}")
        
        action_type = self.current_scene.get_action_type(user_choice_adjusted)
        
        if action_type == "story":
            self.handle_user_story_choice(user_choice_adjusted)
        elif action_type == "enter_dungeon":
            user_choice_action = self.current_scene.get_action(user_choice_adjusted)
            self.context.state = "dungeon"
            self.context.event_bus.emit("enter_dungeon", user_choice_action)
        elif action_type == "end_game":
            self.context.inputSystem.stop_input()
        
    def handle_user_story_choice(self, user_choice_adjusted):
        next_level = self.current_scene.get_next_level(user_choice_adjusted)
        self.context.current_level = next_level
        next_scene = self.current_scene.get_next_scene(user_choice_adjusted)
        resolved = self.resolve_scene_id(next_scene)

        self.context.event_bus.emit(
            "story_load_scene",
            {"load_scene": {"scene": resolved}}
        )
        
    
    def load_scene(self, scene_id: str):
        if scene_id not in self.scenes:
            self.context.loggingSystem.log_error(
                f"Scene not found: {scene_id}"
            )
            return

        self.current_scene = self.scenes[scene_id]

        self.context.event_bus.emit(
            "add_text",
            {"display_text": self.current_scene.get_text()}
        )

        for choice in self.current_scene.get_choices_as_text():
            self.context.event_bus.emit(
                "add_text",
                {"display_text": choice}
            )

        
    def handle_load_scene(self, choice: dict):
        data = choice.get("load_scene")
        if not data:
            self.context.loggingSystem.log_error("Invalid story_load_scene event")
            return

        scene_id = data["scene"]

        resolved_scene = (
            scene_id if ":" in scene_id
            else f"base:{scene_id}"
        )

        self.load_scene(resolved_scene)