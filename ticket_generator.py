class TicketGenerator:
    def __init__(self):
        self.counters = {
            "CLG": {"N": 0, "P": 0},
            "GIN": {"N": 0, "P": 0},
            "PED": {"N": 0, "P": 0},
            "GER": {"N": 0, "P": 0},
            "ORT": {"N": 0, "P": 0},
        }

    def generate(self, specialty, service_type):
        prefix = specialty.upper()
        type_code = "P" if service_type.lower() in ["preferential", "p"] else "N"
        self.counters[prefix][type_code] += 1
        number = self.counters[prefix][type_code]
        return f"{prefix}{type_code}{number:03d}"
