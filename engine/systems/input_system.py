import keyboard
import threading

class InputSystem:
    def __init__(self, context):
        self.context = context
        self.run_input = True
        self.input_thread = threading.Thread(target=self.handle_input)
        self.start_input()
    
    def handle_input(self):
        while self.run_input:
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN:
                if event.name == "*":
                    self.stop_input()
                    continue

                if self.context.state == "story":
                    self.context.event_bus.emit("ACTION", {"input": event.name})
                    continue
                
                self.context.event_bus.emit("player_input", {"input": event.name})
    
    def start_input(self):
        self.run_input = True
        self.input_thread.start()
    
    def stop_input(self):
        self.run_input = False