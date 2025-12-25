import os
import json
from utils.Scene import Scene

class StoryManager:
    def __init__(self, context):
        self.context = context
        
        self.current_scene = None
        
        self.root_dir = os.path.dirname(os.path.dirname(__file__))  
        
        self.handle_subscription()
    
    def handle_subscription(self):
        self.context.event_bus.subscribe("story_load_scene", self.handle_load_scene)
        self.context.event_bus.subscribe("story_choice_made", self.handle_user_story_choice)
        
        
    def handle_user_story_choice(self, choice):
        # Get the choice the user selected
        user_choice_num = int(choice["input"])
        user_choice_adjusted = user_choice_num - 1
        user_choice_text = self.current_scene.get_choice(user_choice_adjusted)
        self.context.loggingSystem.log_info(f"User selected choice {user_choice_num} which maps to choice {user_choice_adjusted}: {user_choice_text}")
        # self.context.event_bus.emit("add_text", {"display_text": f"You selected choice: [{user_choice_num}]"})
       
        new_state = {"level": self.current_scene.get_next_level(user_choice_adjusted), "scene": self.current_scene.get_next_scene(user_choice_adjusted)}
        self.context.event_bus.emit("story_load_scene", {"load_scene": new_state})
        
    def load_scene(self, level: str, scene_name: str) -> None:
        """
        Handles loading a scene and creating the scene
        
        :param level: The level where the scene (json) is located
        :type level: str
        :param scene_name: The name of the scene (filename) without ".json"
        :type scene_name: str
        """
        path = os.path.join(
            self.root_dir,
            "story",
            "levels",
            f"level_{level}",
            f"{scene_name}.json"
        )

        with open(path, "r", encoding="utf-8") as f:
            scene_data = json.load(f)
            self.current_scene = Scene(scene_data)
            self.context.event_bus.emit("add_text", {"display_text": self.current_scene.get_text()})
            for choice in self.current_scene.get_choices_as_text():
                self.context.event_bus.emit("add_text", {"display_text": choice})
        
    
    def handle_load_scene(self, choice: dict) -> None:
        if choice['load_scene']:
            level = choice['load_scene']['level']
            scene = choice['load_scene']['scene']
            self.load_scene(level, scene)
            return
            
        self.context.loggingSystem.log_error("Invalid story_choice event data")
    