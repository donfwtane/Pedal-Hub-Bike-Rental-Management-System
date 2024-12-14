class Customer:
    def __init__(self, first_name, last_name, phone):
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone

    def to_dict(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone": self.phone,
        }

    @staticmethod
    def from_dict(data):
        return Customer(
            first_name=data["first_name"],
            last_name=data["last_name"],
            phone=data["phone"]
        )