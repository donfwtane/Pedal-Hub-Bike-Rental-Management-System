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
        customer = customer.from_dict(data["customer"])
        bike = BikeDetails.from_dict(data["bike"])
        return Booking(
            customer=customer,
            bike=bike,
            duration_hours=data["duration_hours"],
            total_cost=data["total_cost"],
            status=data["status"]
        )