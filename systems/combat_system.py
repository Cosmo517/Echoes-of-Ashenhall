class CombatSystem:
    def __init__(self, context):
        self.context = context
        self.handle_subscriptions()
    
    def handle_subscriptions(self):
        self.context.event_bus.subscribe("combat_initiated", self.get_combat_start)
    
    def resolve_combat(self, attacker, defender):
        raise NotImplementedError
    
    def get_combat_start(self):
        # get attacker, get defender, call resolve_combat
        raise NotImplementedError