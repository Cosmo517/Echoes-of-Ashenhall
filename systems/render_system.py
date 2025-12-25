class RenderSystem:
    def __init__(self, context):
        self.context = context
        self.text_to_draw = []
        
        self.handle_subscriptions()
        
    def draw_dungeon(self, dungeon_map):
        raise NotImplementedError
    
    def add_text(self, text):
        print(text['display_text'])
        # self.text_to_draw.append(text['display_text'])
    
    def handle_subscriptions(self):
        self.context.event_bus.subscribe("dungeon_updated", self.draw_dungeon)
        self.context.event_bus.subscribe("add_text", self.add_text)