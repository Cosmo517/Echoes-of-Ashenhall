class EventBus:
    def __init__(self, context):
        self.context = context
        self.subscribers = {}
    
    def subscribe(self, event_name, callback):
        """Registers a function to listen for an event"""
        if event_name not in self.subscribers:
            self.subscribers[event_name] = []
        owner = callback.__self__.__class__.__name__
        self.context.loggingSystem.log_event_subscribe(event_name, owner)
        self.subscribers[event_name].append(callback)
    
    def emit(self, event_name, data=None):
        """Tell all listeners that this event happened"""
        self.context.loggingSystem.log_event_emit(event_name, data)
        if event_name not in self.subscribers:
            return
        
        for callback in self.subscribers[event_name]:
            owner = callback.__self__.__class__.__name__
            self.context.loggingSystem.log_event_dispatch(owner, event_name)
            callback(data)