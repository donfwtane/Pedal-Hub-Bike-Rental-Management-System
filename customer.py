class Customer:

    # Initializes the customer information
    def __init__(self, first_name, last_name, phone):
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone

    # Turns the customer object into a dictionary format
    def to_dict(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone": self.phone,
        }

    # Static method to create a Customer object from a dictionary
    @staticmethod
    def from_dict(data):
        # Create and return a new Customer instance using the provided dictionary data
        return Customer(
            first_name=data["first_name"],   # Extract the first name from the dictionary
            last_name=data["last_name"],     # Extract the last name from the dictionary
            phone=data["phone"]              # Extract the phone number from the dictionary
        )
