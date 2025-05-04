from user import User

class Attendant(User):
    
    def __init__(self, name, age, counter):
        super().__init__(name, age)
        self.counter = counter
        self.counter_states: list = ["available", "attending"]
        self.current_state: str = ""
        self.can_attend: bool = True
        
    def __str__(self):
        return f"{self.name} - ({self.age} | {self.counter})"

    def transition_state(self):
        if self.current_state in self.counter_states:
            match self.current_state:
                case "available":
                    self.can_attend = True
                case "attending":
                    self.can_attend = False
    
    def start_attendance(self):
        self.current_state = "attending"
        self.transition_state()

    def finish_attendance(self):
        self.current_state = "available"
        self.transition_state()
