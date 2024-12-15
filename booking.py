from bikedetails import BikeDetails

""" 
This class handles everything related to a booking. A booking includes information about the customer (who rented the bike), the bike itself (which bike was rented), 
how long the bike was rented for (in hours), the total cost of the rental, and the booking status (which can be "Active", "Completed", etc.).
It has methods to convert the booking into a dictionary (for saving or sharing) and create a booking from a dictionary (like when loading data from a file).
"""


class Booking:
    def __init__(self, customer, bike, duration_hours, total_cost, status="Active"):
        self.customer = customer
        self.bike = bike
        self.duration_hours = duration_hours
        self.total_cost = total_cost
        self.status = status


    def to_dict(self):
        return {
            "customer": self.customer.to_dict(),
            "bike": self.bike.to_dict(),
            "duration_hours": self.duration_hours,
            "total_cost": self.total_cost,
            "status": self.status
        }

    @staticmethod
    def from_dict(data):
        customer = customer.from_dict(data["customer"])   # Convert customer data back to Customer object
        bike = BikeDetails.from_dict(data["bike"])        # Convert bike data back to BikeDetails object
        return Booking(
            customer=customer,
            bike=bike,
            duration_hours=data["duration_hours"],
            total_cost=data["total_cost"],
            status=data["status"]
        )
