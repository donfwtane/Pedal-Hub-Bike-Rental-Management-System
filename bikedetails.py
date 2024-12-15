"""
A class representing the details of a bike in a rental system. This class holds information about a bike and includes methods
to calculate rental costs and to convert the bike's details to and from dictionary format for storage or retrieval.
"""
class BikeDetails:
    
    def __init__(self, bike_id, bike_type, size, color, rental_price, available=True):
        self.bike_id = bike_id
        self.bike_type = bike_type
        self.size = size
        self.color = color
        self.rental_price = rental_price
        self.available = available
        
    
    def calculate_rental_cost(self, hours):
        return self.rental_price * hours
    
    
   
    # Used to convert an instance of the class back into a dictionary, useful for storing bike information in databases or files.
    def to_dict(self):
        return {
            "bike_id": self.bike_id,
            "bike_type": self.bike_type,
            "size": self.size,
            "color": self.color,
            "rental_price": self.rental_price,
            "available": self.available
        }


    """ 
    This is a static method that creates an instance of BikeDetails from a dictionary.
    It takes a dictionary (data) as input and extracts the required values to initialize a new BikeDetails object.
    """
    @staticmethod
    def from_dict(data):
        return BikeDetails(
            bike_id=data["bike_id"],
            bike_type=data["bike_type"],
            size=data["size"],
            color=data["color"],
            rental_price=data["rental_price"],
            available=data.get("available", True)  # Default to True if 'available' key is missing
        )
