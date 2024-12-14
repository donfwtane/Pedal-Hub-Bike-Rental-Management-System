import os
import json
from customer import Customer
from bikedetails import BikeDetails
from booking import Booking
from datamanager import DataManager


class PedalHub:
    ADMIN_USERNAME = "admin"
    ADMIN_PASSWORD = "youradmin123"
    BIKE_FILE = "bike_inventory.json"        # File to store bike details
    BOOKINGS_FILE = "bookings.json"          # File to store boooking details
    HISTORY_FILE = "rental_history.json"     # File to store rental history

    def __init__(self):
        #Initializes the PedalHUb class by loading data from files.
        self.bike_inventory = []     # List to store bike details
        self.bookings = []           # List to store active rentals
        self.rental_history = []     # List to store completed rentals
        try:
            self.load_data()        # Load existing data from files
        except Exception as e:
            print(f"Error initializing PedalHub: {e}")

    #Clears the console/terminal screen based on the operating system
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    # Load data from JSON files
    def load_data(self):
        try:
            # Load the bike inventory, rentals/bookings, and rental history
            self.bike_inventory = self.load_from_file(self.BIKE_FILE, BikeDetails.from_dict)
            self.bookings = self.load_from_file(self.BOOKINGS_FILE)
            self.rental_history = self.load_from_file(self.HISTORY_FILE)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading data: {e}. Files will be recreated on save.")  # Handle errors if files are missing or corrupted

    # Save current data (bikes, bookings, rental history) to respective files
    def save_data(self):
        try:
            self.save_to_file(self.BIKE_FILE, [bike.to_dict() for bike in self.bike_inventory])
            self.save_to_file(self.BOOKINGS_FILE, self.bookings)
            self.save_to_file(self.HISTORY_FILE, self.rental_history)
        except Exception as e:
            print(f"Error saving data: {e}")

    # Helper function to load data from a file and transform it if necessary
    @staticmethod
    def load_from_file(filename, transform=None):
        if not os.path.exists(filename): # Return empty list if file doesn't exist
            return []
        with open(filename, "r") as file: 
            data = json.load(file)  # Read data from the file in JSON format
            if transform: # If a transformation function is provided, use it to convert data items
                return [transform(item) for item in data]
            return data  # Return the raw data

    # Helper function to save data to a file in JSON format
    @staticmethod
    def save_to_file(filename, data):
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)  # Helper function to save data to a file

    def run(self):
        try:
            print("\n\nLooking for a bike to rent for a day? Welcome to PEDALHUB! \nYour go-to destination for convenient, eco-friendly, and affordable bike rentals.")
            print("Whether you're commuting, sightseeing, or just out for some fun, we've got the perfect bike for you!")

            while True:
                self.display_main_menu()
                choice = self.get_user_input("Enter your choice: ", int)

                if choice == 1:
                    self.view_bikes()
                elif choice == 2:
                    self.rent_bike()
                elif choice == 3:
                    self.admin_dashboard()
                elif choice == 4:
                    print("\nThank you for choosing Pedal Hub! See you next time!")
                    self.save_data()  # Save all data before exiting
                    break
                else:
                    print("Invalid choice. Try again.")
        except KeyboardInterrupt:
            print("\nProgram terminated by user.")   # Handle manual interruption of the program
        except Exception as e:
            print(f"An unexpected error occured: {e}")

    def display_main_menu(self):
        
        print("\n\n=========================================================")
        print("|\t --- PedalHub (Bike Rental System)--- \t\t|")
        print("|\t [1] View Bikes   \t\t\t\t|")
        print("|\t [2] Rent a Bike   \t\t\t\t|")
        print("|\t [3] Admin Dashboard \t\t\t\t|")
        print("|\t [4] Exit   \t\t\t\t\t|")
        print("=========================================================")


    def view_bikes(self):
        try:
            self.clear_screen()
            # A bike size chart as a guide for users when choosing the right bike for them
            print("\t\tMOUNTAIN/ROAD BIKE SIZE CHART\t\t\t\t\t\t\t\t  CHILDREN BIKE SIZE CHART\n")
            print("RIDER HEIGHT IN CM\tFRAME SIZE IN CM\t  STATED SIZE\t\t\t  RIDER AGE\t  RIDER HEIGHT IN CM\t    WHEEL SIZE (inches)\t    STATED SIZE")
            print("---------------------------------------------------------------------------------------------------------------------------------------------------------------")
            print("     120-135\t\t   18-20\t\t      XXS\t\t\t     4-6\t\t110-120\t\t\t    16\"\t\t\t S")
            print("     135-145\t\t   22-24\t\t      XS\t\t\t     5-8\t\t115-135\t\t\t    20\"\t\t\t M")
            print("     148-158\t\t   13-15\t\t      S\t\t\t\t     8-11\t\t135-145\t\t\t    24\"\t\t\t L")
            print("     158-165\t\t   15-17\t\t      M\t\t\t")
            print("     160-175\t\t   17-18\t\t      L\t\t\t")
            print("     175-185\t\t   19-20\t\t      XL\t\t\t")
            print("     185-200\t\t   21-22\t\t      XXL\t\t\t")
            print("***************************************************************************************************************************************************************\n\n")
    
            
            print("\n*|---------- List of Bikes ----------|*\n")
            if not self.bike_inventory:
                print("No bikes available at the moment.")
                return

            # Display the bike inventory in a structured tabular format
            print(f"{'Bike ID':<15} {'Type':<20} {'Size':10} {'Color':<15} {'Rental Price (per hour)':<30} {'Available':<20}")
            print("=" * 110) 

             # Loop through the bikes in the inventory and display each bike's details
            for bike in self.bike_inventory:
                availability = "Yes" if bike.available else "No"
                print(f"{bike.bike_id:<15} {bike.bike_type:<20} {bike.size:<10} {bike.color:<15} Php {bike.rental_price:<27.2f} {availability:<20}")
        
        except Exception as e:
            print(f"Error displaying bikes: {e}")

    def rent_bike(self):
        try: 
            self.clear_screen()
            print("\n*|---------- Rent a Bike ----------|*")
            if not self.bike_inventory:
                print("No bikes available to rent. Please check again later.")
                return

            bike_id = input("Enter Bike ID to rent: ").strip()
            
            # Search for the selected bike in the inventory
            selected_bike = None
            for bike in self.bike_inventory:
                if bike.bike_id.lower() == bike_id.lower():
                    selected_bike = bike
                    break
                
            if not selected_bike:
                print("Bike not found.")
                return
            
            if not selected_bike.available:
                print(f"Bike ID {bike_id} is currently not available for rent. Please select a different bike.")
                return

                
            print("\n*|-------- Customer Details --------|*")
            while True:
                customer_firstName = input("Enter your First Name: ")
                if customer_firstName and customer_firstName.isalpha():
                    break
                print("Invalid input. First name cannot be empty and must contain letters only.")
            
            while True:
                customer_lastName = input("Enter your Last Name: ").strip()
                if customer_lastName and customer_lastName.isalpha():
                    break
                print("Invalid input. Last name cannot be empty and must contain letters only.")

            while True:
                customer_phone = input("Enter your Phone Number: ").strip()
                if customer_phone and customer_phone.isdigit():
                    break
                print("Invalid input. Phone number cannot be empty and must contain digits only.")

            # Rental duration validation
            print("\nChoose the rental duration: ")
            print("[1] Hours")
            print("[2] Minutes")
            
            while True:
                duration_choice = self.get_user_input("Select an option (1 or 2): ", int, min_value=1, max_value=2)

                if duration_choice == 1:
                    duration = self.get_user_input("Enter duration in hours: ", int)
                    if duration > 1:
                        duration_hours = duration
                        break
                    print("Rental duration must be greater than 1 hour.")
                elif duration_choice == 2:
                    duration = self.get_user_input("Enter duration in minutes: ", int)
                    if duration > 1:
                        duration_hours = duration / 60
                        break
                    print("Rental duration must be greater than 60 minutes.")

            total_cost = bike.calculate_rental_cost(duration_hours)

            # Create a booking record for the rental
            booking = {
                "customer_firstName": customer_firstName,
                "customer_lastName": customer_lastName,
                "customer_phone": customer_phone,
                "bike_id": bike.bike_id,
                "rental_hours": duration_hours,
                "total_cost": total_cost,
                "status": "Active"  # Mark the booking as active initially
            }
            
            bike.available = False  # Mark the bike as rented (not available)
            
            # Add the booking to the list of active bookings and rental history
            self.bookings.append(booking)
            self.rental_history.append({**booking, "status": "Active"})
            
            # Save updated data to the files
            self.save_data()
            print(f"\nRental confirmed. Bike {bike_id} has been rented by {customer_firstName}.\nTotal Cost: Php {total_cost:.2f}")
            return
                    
        except Exception as e:
            print(f"Error renting bike: {e}")
            

    def admin_dashboard(self):
        if not self.authenticate_admin():
            print("Access Denied. Returning to Main Menu...")
            return
        
        self.clear_screen
    
        while True:
            print("\n=================================================")
            print("|\t --- Admin Dashboard--- \t\t|")
            print("|\t [1] Add New Bike   \t\t\t|")
            print("|\t [2] Delete Bike \t\t\t|")
            print("|\t [3] Mark Rentals as Completed  \t|")
            print("|\t [4] View Rentals \t\t\t|")
            print("|\t [5] Back To Main Menu   \t\t|")
            print("=================================================")

            choice = self.get_user_input("Enter your choice: ", int)

            if choice == 1:
                self.add_new_bike()
            elif choice == 2:
                self.delete_bike()
            elif choice == 3:
                self.mark_bike_completed()
            elif choice == 4:
                self.view_bookings()
                input("Press Enter to return to Admin Dashboard...")
            elif choice == 5:
                print("Returning to Main Menu...")
                self.clear_screen()
                break
            else:
                print("Invalid choice. Try again.")

    def authenticate_admin(self):
        self.clear_screen()
        print("\n*|---------- Admin Login ----------|*")
        username = input("Enter Admin Username: ").strip()
        password = input("Enter Admin Password: ").strip()
        return username == self.ADMIN_USERNAME and password == self.ADMIN_PASSWORD

    def add_new_bike(self):
        self.clear_screen()
        self.view_bikes()
        print("\n\n*|---------- Add Bike -----------|*")
        bike_id = input("\nEnter Bike ID: ").strip()
        bike_type = input("Enter the type of Bike: ").strip()
        size = input("Enter the size: ").strip()
        color = input("Enter Color: ").strip()
        rental_price = self.get_user_input("Enter Rental Price per Hour: ", float)

        self.bike_inventory.append(
            BikeDetails(bike_id, bike_type, size, color, rental_price)
        )
        self.save_data()  # Save the bike data immediately after adding
        print("Bike added successfully!")
        
    def delete_bike(self):
        self.clear_screen()
        self.view_bikes()
        print("*|---------- Delete Bike ----------|\n*")
        bike_id = input("Enter Bike ID to delete: ").strip()
        
        # Search for the bike in the inventory
        for bike in self.bike_inventory:
            if bike.bike_id.lower() == bike_id.lower():
                self.bike_inventory.remove(bike)
                self.save_data()  # Save the updated inventory to the file
                print(f"Bike {bike_id} has been deleted successfully.")
                return

        print(f"Bike with ID {bike_id} not found in inventory.")    


    def mark_bike_completed(self):
        self.clear_screen()
        print("\n*|---------- Mark Bike as Completed ----------|*")

        if not self.bookings:
            print("No active rentals to complete.")
            return  # Return after showing message, preventing further execution

        bike_id = input("Enter the Bike ID to mark as completed: ").strip()

        for booking in self.bookings:
            if booking['bike_id'].lower() == bike_id.lower() and booking.get('status') == 'Active':
                booking['status'] = 'Completed'

                # Find the corresponding bike and mark it as available again
                for bike in self.bike_inventory:
                    if bike.bike_id.lower() == bike_id.lower():
                        bike.available = True  # Mark the bike as available again
                        break
                
                self.save_data()  # Save updated bike inventory and booking status
                booking_found = True
                print(f"Rental for Bike ID {bike_id} has been marked as completed.\n")
                input("Press Enter to return to Admin Dashboard...")
                return  # Ensure we return here so that it doesn't go back to the dashboard immediately

        print(f"No active rental found for Bike ID {bike_id}.\n")
        input("Press Enter to return to Admin Dashboard...")  # Wait for input to return to Admin Dashboard

    def view_bookings(self):
        self.clear_screen()
        print("\n*|---------- Rentals ----------|*")

        if not self.bookings:
            print("No rentals available at the moment.")
            return

        # Display each booking in a tabular format
        for index, booking in enumerate(self.bookings, start=1):
            print(f"\nRental #{index}")
            print(f"  First Name     : {booking['customer_firstName']}")
            print(f"  Last Name      : {booking['customer_lastName']}")
            print(f"  Phone Number   : {booking['customer_phone']}")
            print(f"  Bike ID        : {booking['bike_id']}")
            print(f"  Rental Hours   : {booking['rental_hours']}")
            print(f"  Total Cost     : Php {booking['total_cost']:.2f}")
            print(f"  Status         : {booking.get('status', 'Active')}")  # Display status
            print("-" * 40)
            
        # Deletion of bike
        while True:
            delete_choice = input("Do you want to delete a rental? (yes/no): ").strip().lower()
            if delete_choice == "yes":
                # Ask for the booking number to delete
                try:
                    booking_number = int(input("Enter the rental number to delete: ").strip())
                    if 1 <= booking_number <= len(self.bookings):
                        removed_booking = self.bookings.pop(booking_number - 1)

                        # Update bike availability if the deleted booking is active
                        if removed_booking['status'] == 'Active':
                            for bike in self.bike_inventory:
                                if bike.bike_id.lower() == removed_booking['bike_id'].lower():
                                    bike.available = True
                                    break

                        # Save updated bookings and bike inventory directly to files
                        self.save_to_file(self.BOOKINGS_FILE, self.bookings)
                        self.save_to_file(self.BIKE_FILE, [bike.to_dict() for bike in self.bike_inventory])
                        print(f"Rental #{booking_number} has been successfully deleted from the file.")
                    else:
                        print("Invalid booking number. Please try again.")
                except ValueError:
                    print("Invalid input. Please enter a valid booking number.")
            elif delete_choice == "no":
                print("Returning to Admin Dashboard...")
                break
            else:
                print("Invalid choice. Please enter 'yes' or 'no'.")
            
            
    @staticmethod
    def get_user_input(prompt, input_type, min_value=None, max_value=None):
        while True:
            try:
                value = input_type(input(prompt).strip())
                
                # Checks if a minimum value is set, and ensure the entered value is not less than the minimum
                if min_value and value < min_value:
                    print(f"Value must be at least {min_value}. Try again.")
                    continue   # If the input is too low, ask for input again
                
                # Check if a maximum value is set, and ensure the entered value is not greater than the maximum
                if max_value and value > max_value:
                    print(f"Value must be at most {max_value}. Try again.")
                    continue  # If the input is too high, ask for input again
                return value
            except ValueError:
                print("Invalid input. Please try again.")

if __name__ == "__main__":         
    pedal_hub = PedalHub()  # Create instance of PedalHub
    pedal_hub.run()  # Start the system
