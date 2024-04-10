from datetime import datetime
from math import ceil
import json

cars_dict = {}

class Car():
    """
	Attributes:
	reg_num: The registration number of the car.
	owner: The owner of the car.
	car_class: The car's weight class. Can be light, medium, or heavy.
    balance: The balance of the car's account.
    parking_history: A list of all parkings the car has made.
	"""
    def __init__(self, reg_num, owner, car_class, balance=0, parking_history=[]):
        self.reg_num = reg_num
        self.owner = owner
        self.car_class = car_class
        self.balance = balance
        self.parking_history = parking_history
    
    def __str__(self):
        return f"Information about [{self.reg_num}]:\n┗━ Owner: {self.owner}\n┗━ Class: {self.car_class}\n┗━ Balance: {self.balance}\n"
    
    def car_format(self):
        return {
                "reg_num": self.reg_num,
                "owner": self.owner,
                "car_class": self.car_class,
                "balance": self.balance,
                "parking_history": self.parking_history
                }

    def add_parking(self, parking):
        self.parking_history.append(parking.parking_format())

    def show_parking(self):
        parking = self.parking_history
        if not parking:
            print(f"\nNo parkings has been registered for [{self.reg_num}].")
        else:
            total_debt = 0
            for i, parking in enumerate(self.parking_history):
                print(f"\nParking {i+1}:\nDate: {parking['date']}\nTime: {parking['start_time']} - {parking['end_time']} ({parking['total_time']})\nCost: {parking['total_cost']}")
                total_debt += parking["total_cost"]
            print(f"\nTotal debt: {total_debt}")
            return i

    def pay_parking(self):
        print("\nList of all parkings for this car:")
        i = self.show_parking()
        pay_loop = True
        while pay_loop:
            park_num = int_input(f"\nWhich parking entry would you like to pay for? (1-{i+1})\n>> ")
            try:
                cost = self.parking_history[park_num-1]["total_cost"]
                if cost == 0:
                    self.parking_history[park_num-1]["total_cost"] = 0
                    return "Parking has already been paid for."
                else:
                    pay_loop = False
            except IndexError:
                print("That is not an option.")
        
        if self.balance != 0:
            print(f"\nThe cost for parking {i+1} is {cost}.")
            balance_loop = True
            while balance_loop:
                use_balance = input("Would you like to use your balance to pay for the parking? (yes/no)\n>> ")
                print()
                if use_balance == "yes":
                    if self.balance == cost:
                        self.balance, cost, self.parking_history[park_num-1]["total_cost"] = 0, 0, 0
                        cars_dict[self.reg_num] = self.car_format()
                        return f"Parking paid in full with your balance."
                    elif self.balance < cost:
                        cost -= self.balance
                        print(f"Payment of {self.balance} was made. {cost} remains.")
                        self.balance = 0
                    else:
                        self.balance -= cost
                        self.parking_history[park_num-1]["total_cost"] = 0
                        print(f"Parking paid in full. New balance: {self.balance}.")
                    balance_loop = False
                elif use_balance == "no":
                    balance_loop = False
                else:
                    print("Invalid input. Please enter yes or no.")

        if cost != 0:
            payment_loop = True
            while payment_loop:
                payment = int_input("\nHow much would you like to pay?\n(If you pay more than the parking's fine, it will be added to a total balance.)\n>> ")
                print()
                if payment < cost:
                    print(f"Not enough money. At least {cost} is required.")
                elif payment == cost:
                    self.parking_history[park_num-1]["total_cost"] = 0
                    print("Parking paid in full.")
                    payment_loop = False
                else:
                    self.balance = self.balance + (payment - cost)
                    self.parking_history[park_num-1]["total_cost"] = 0
                    print(f"Parking paid in full. {self.balance} was added to your balance.")
                    payment_loop = False
        cars_dict[self.reg_num] = self.car_format()
        return "Payment completed. Thank you!"

class Parking():
    """
	Attributes:
	start_time: The parking's start time
	end_time: The parking's end time
    car_class: The car's weight class. Can be light, medium, or heavy.
    date: The date of the parking
    total_time: The total time the car was parked
    total_cost: The total cost of the parking
	"""
    def __init__(self, start_time, end_time, car_class):
        self.start_time = start_time
        self.end_time = end_time
        self.car_class = car_class
        self.date = str(datetime.now().date())
        self.total_time = self.calc_time()
        self.total_cost = self.calc_cost()
    
    def __str__(self):
        return f"┗━ Time: {self.start_time} - {self.end_time} ({self.total_time})\n┗━ Cost: {self.total_cost}"
    
    def parking_format(self):
        return {
                "date": self.date,
                "start_time": self.start_time,
                "end_time": self.end_time,
                "total_time": self.total_time,
                "total_cost": self.total_cost
                }

    def calc_time(self):
        y, m, d = str(self.date).split("-")

        start_hour, start_min = self.start_time.split(":")
        end_hour, end_min = self.end_time.split(":")

        ts1 = datetime(int(y), int(m), int(d), int(start_hour), int(start_min))
        ts2 = datetime(int(y), int(m), int(d), int(end_hour), int(end_min))

        delta = ts2 - ts1
        
        return str(delta)

    def calc_cost(self):
        hour, minute, _ = self.total_time.split(":")

        time = int(hour) + int(minute) / 60
        rounded_time = ceil(time * 2) / 2
        
        if self.car_class == "light":
            cost_per_hour = 15
        elif self.car_class == "medium":
            cost_per_hour = 20
        else:
            cost_per_hour = 25
        
        return round(cost_per_hour * rounded_time)

def write_to_file(datafile):
    with open(datafile, "w", encoding="utf8") as file:
        json.dump(cars_dict, file, indent=4)

def read_from_file(datafile):
    while True:
        try:
            with open(datafile, "r", encoding="utf8") as file:
                loaded_data = json.load(file)
                file_objects = {}
                for reg_num, car_data in loaded_data.items():
                    file_objects[reg_num] = Car(**car_data)
                    cars_dict[reg_num] = car_data
                    print(file_objects[reg_num])
                
                print(f"\nLoading {len(loaded_data)} entities from file...")
            return loaded_data
        except FileNotFoundError:
            print("\nFile not found. Please try again.")
        except json.decoder.JSONDecodeError:
            print("\nInvalid file format. Make sure to input a JSON-file.")
        datafile = input("Enter filename: ")

def int_input(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a number.")

def parking_input(prompt):
    while True:
        try:
            time = input(prompt)
            hours, mins = time.split(":")
            if int(hours) in range(0, 24) and int(mins) in range(0, 60):
                # if time[0]== "0":
                #     time = time[1:]
                return time
            else:
                raise ValueError
        except ValueError:
            print("Please follow the format HH:MM.")

def reg_check(prompt):
    while True:
        try:
            reg_num = input(prompt)
            car = cars_dict[reg_num]
            car[reg_num] = Car(car["reg_num"], car["owner"], car["car_class"], car["balance"], car["parking_history"])
            return reg_num, car[reg_num]
        except KeyError:
            print(f"Car [{reg_num}] not found in database. (You can add a new car from the main menu)")

def add_car(reg_num, owner, car_class, balance=0, parking_history=[]):
    added_car = Car(reg_num, owner, car_class, balance, parking_history)
    cars_dict[added_car.reg_num] = added_car.car_format()
    return f"\nCar [{reg_num}] was added to database."

def menu():
    print("""
            Park Dark Mark Bark
-------------------------------------------
{0} TESTING
          
{1} New parking
{2} Read file & history
{3} Add new car
{4} Parking history & costs
{5} Pay for parking
{6} Exit
          """)
    
    menu_loop = True
    while menu_loop:
        choice = int_input(">> ")
        if choice in range(0, 7):           # NOTE Ändra till 1-6 när TESTING tas bort
            return choice
        else:
            print("Invalid input. Please try again.")

def execute(choice, cars_dict=cars_dict):
    loop = True
    while loop:
        if choice == 1:     # New parking
            reg_num, car = reg_check("Registration number: ")
            start_time = parking_input("Start time (HH:MM): ")

            while True:
                end_time = parking_input("End time (HH:MM): ")
                
                start_h, start_m = (int(t) for t in start_time.split(":"))
                end_h, end_m = (int(t) for t in end_time.split(":"))
                
                if end_h < start_h or (end_h <= start_h and end_m < start_m) or (end_h == start_h and end_m == start_m):
                    print("End time must be a later time than start time.")
                    print("If you'd like to park over midnight, please make two separate parkings.")
                else:
                    break

            parking = Parking(start_time, end_time, car.car_class)
            car.add_parking(parking)
            cars_dict[reg_num] = car.car_format()
            
            print("\nParking confirmed. Details below:")
            print(parking)

        elif choice == 2:     # Read file & history
            data = input("Enter filename: ")
            read_from_file(data)
            print("Database loaded from file.")
        
        elif choice == 3:     # Add new car
            new_car_loop = True
            while new_car_loop:
                reg_num = input("Registration number of new car: ")
                if reg_num in cars_dict:
                    print("Car already exists in database. Please enter a new registration number.")
                else:
                    new_car_loop = False

            owner = input("Owner of the car: ")
            
            car_class_loop = True                                                               # NOTE BUG Skapa egen funktion för att välja klass baserat på vikt
            while car_class_loop:
                car_class = input("Car class (light, medium, heavy): ")
                if car_class not in ["light", "medium", "heavy"]:
                    print("Invalid class. Please enter light, medium, or heavy.")
                else:
                    car_class_loop = False

            print("Adding car to database...")
            print(add_car(reg_num, owner, car_class))

        elif choice == 4:     # Parking history & costs
            reg_num, car = reg_check("Registration number of car to show history for: ")
            car.show_parking()

        elif choice == 5:     # Pay for parking
            reg_num, car = reg_check("Registration number of car to pay for: ")
            print(car.pay_parking())
            
        elif choice == 6:     # Avsluta NOTE fixa utan break
            reg_num, car = reg_check("Reg num: ")
            print(car)
            break

        elif choice == 0:
            # car1 = Car("ABC123", "Someone", "light")
            
            # parking1 = Parking("12:00", "14:30", car1.car_format()["car_class"])
            # car1.add_parking(parking1)
            # parking2 = Parking("16:23", "21:58", car1.car_format()["car_class"])
            # car1.add_parking(parking2)

            # cars_dict[car1.reg_num] = car1.car_format()
            # print("\n" + str(car1) + "\n")
            # car1.show_parking()

            cars_dict = read_from_file("data.json")
            # print(cars_dict)

        print()
        choice = menu()
        print()
    write_to_file("data.json")

def main():
    execute(menu())

if __name__ == "__main__":
    main()