class Scene:
    def __init__(self, scene_json, mod_id):
        self.scene_id = scene_json["scene_id"]
        self.level = scene_json["level"]
        self.text = scene_json["text"]
        self.choices = scene_json["choices"]
        self.mod_id = mod_id

    def get_scene_id(self):
        return self.scene_id
    
    def get_level(self):
        return self.level
    
    def get_next_level(self, choice):
        if self.choices[choice]["action"]["next_level"]:
            return self.choices[choice]["action"]["next_level"]
        
        return None
    
    def get_text(self):
        return self.text
    
    def get_choice(self, choice):
        return self.choices[choice]
    
    def get_choices(self):
        return self.choices

    def get_choices_as_text(self):
        choice_text = []
        for index, choice in enumerate(self.choices, start=1):
            choice_text.append(f"{index}: {choice["text"]}")
            
        return choice_text

    def get_next_scene(self, choice):
        return self.choices[choice]["action"]["next_scene"]
    
    def get_action_type(self, choice):
        return self.choices[choice]["action"]["type"]
    
    def get_action(self, choice):
        return self.choices[choice]["action"]