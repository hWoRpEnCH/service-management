from user import User

class Patient(User):
    def __init__(self, name, age, service_type, specialty, complaint, ticket):
        super().__init__(name, age)
        self.service_type = service_type      # "Normal" or "Preferential"
        self.specialty = specialty            # Code: "CG", "GIN", etc.
        self.complaint = complaint
        self.ticket = ticket

    def __str__(self):
        return f"{self.name} ({self.age} years old) - Ticket: {self.ticket} - Specialty: {self.specialty}"