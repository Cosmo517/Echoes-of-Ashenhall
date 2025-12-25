class DungeonManager:
    def __init__(self, context):
        self.context = context
    
    def generate_dungeon(self):
        raise NotImplementedError

    def enemy_turn(self):
        raise NotImplementedError

    def handle_subscriptions(self):
        raise NotImplementedError
    
    def player_exited(self):
        raise NotImplementedError
    
    def dungeon_updated(self):
        raise NotImplementedError