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
        return f"Information about car\n Owner: {self.owner}\n Registration number: {self.reg_num}\n Class: {self.car_class}\n"
    
    def car_format(self):
        return {
                "reg_num": self.reg_num,
                "owner": self.owner,
                "car_class": self.car_class,
                "balance": self.balance,
                "parking_history": self.parking_history
                }
    
    def show_balance(self):
        total_debt = 0
        for fee in self.parking_history:
            total_debt += fee["total_cost"]
        return f"Total debt for {self.reg_num}: {total_debt}"

    def add_parking(self, parking):
        self.parking_history.append(parking.parking_format())

    def show_parking(self):
        parking = self.parking_history
        if not parking:
            print(f"\nNo parkings have been registered with {self.reg_num}.")
        else:
            for i, parking in enumerate(self.parking_history):
                print(f"\nParking {i+1}:\nDate: {parking['date']}\nTime: {parking['start_time']} - {parking['end_time']} ({parking['total_time']})\nCost: {parking['total_cost']}")
            return i

    def pay_parking(self):
        print("List of all parkings for this car:")
        i = self.show_parking()
        parking_number = int_input(f"Which parking entry would you like to pay for? (1-{i+1})\n>> ")
        cost = self.parking_history[parking_number-1]["total_cost"]
        print(f"The cost for parking {i+1}: {cost}")
        
        if self.balance != 0:
            balance_loop = True
            while balance_loop:
                use_balance = input("\nWould you like to use your balance to pay for the parking? (yes/no)\n>> ")
                if use_balance == "yes":
                    if self.balance == cost:
                        self.balance, cost = 0, 0
                        print(f"Parking paid in full. New balance: {self.balance}.")
                    elif self.balance < cost:
                        cost -= self.balance
                        print(f"Payment of {self.balance} was made. {cost} remains.")
                        self.balance = 0
                    else:
                        self.balance -= cost
                        cost = 0
                        print(f"Parking paid in full. New balance: {self.balance}.")
                    balance_loop = False
                elif use_balance == "no":
                    balance_loop = False
                else:
                    print("Invalid input. Please enter yes or no.")

        if cost != 0:
            payment_loop = True
            while payment_loop:
                payment = int_input("How much would you like to pay?\n>> ")
                if payment < cost:
                    print(f"Not enough money. At least {cost} is required.")
                elif payment == cost:
                    cost = 0
                    print("Parking paid in full. Thank you!")
                    payment_loop = False
                else:
                    cost = 0
                    self.balance = payment - cost
                    print(f"Parking paid in full. {self.balance} was added to your balance.")
                    payment_loop = False
            return "Payment completed. Thank you!"
        else:
            return "Parking has already been paid for."

class Parking():
    """
	Attributes:
	start_time: The parking's start time
	end_time: The parking's end time
    car_class: The car's weight class. Can be light, medium, or heavy.
	"""
    def __init__(self, start_time, end_time, car_class):
        self.start_time = start_time
        self.end_time = end_time
        self.car_class = car_class
        self.date = str(datetime.now().date())
        self.total_time = self.calc_time()
        self.total_cost = self.calc_cost()
    
    def __str__(self):
        return f"Time: {self.start_time} - {self.end_time} ({self.total_time})\nCost: {self.total_cost}"
    
    def parking_format(self):
        return {
                "date": self.date,
                "start_time": self.start_time,
                "end_time": self.end_time,
                "total_time": self.total_time,
                "total_cost": self.total_cost
                }

    def calc_time(self): # BUG Funkar inte om parkeringen sträcker sig över midnatt
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
                
        return cost_per_hour * rounded_time

def write_to_file(datafile):
    with open(datafile, "w") as file:
        json.dump(cars_dict, file, indent=4)

def read_from_file(datafile):
    while True:
        try:
            with open(datafile, "r") as file:
                loaded_data = json.load(file)
                print(f"\nLoaded {len(loaded_data)} entities from file.")
            return loaded_data
        except FileNotFoundError:
            print("\nFile not found. Please try again.")
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
                return time
            else:
                raise ValueError
        except ValueError:
            print("Please follow the format HH:MM.")

def add_car(reg_num, owner, car_class, balance=0, parking_history=[]):
    added_car = Car(reg_num, owner, car_class, balance, parking_history)
    cars_dict[added_car.reg_num] = added_car.car_format()
    return f"\nCar [{reg_num}] was added to database."

def menu():
    print("""
            Park Dark Mark Bark
-------------------------------------------
{0} TESTING (ignore)
          
{1} Ny parkering
{2} Läs in fil med historik
{3} Lägg till ny bil
{4} Parkeringshistorik & kostnader
{5} Betala parkering
{6} Avsluta
          """)
    
    loop = True
    while loop:
        choice = int_input(">> ")
        if choice in range(0, 7):           # NOTE Ändra till 1-6 när TESTING tas bort
            return choice
        else:
            print("Invalid input. Please try again.")

def execute(choice):
    global cars_dict                

    loop = True
    while loop and choice != 7:
        if choice == 1:       # Ny parkering
            reg_num = input("Registration number: ")
            try:
                car = cars_dict[reg_num]

                start_time = parking_input("Start time (HH:MM): ")
                end_time = parking_input("End time (HH:MM): ")
                parking = Parking(start_time, end_time, car["car_class"])
                
                parked_car = Car(car["reg_num"], car["owner"], car["car_class"], car["balance"], car["parking_history"])
                parked_car.add_parking(parking)
                cars_dict[reg_num] = parked_car.car_format()
                
                print("\nParking confirmed. Details below:")
                print(parking)
            except KeyError:
                restart_loop = True
                print("Car not found. Would you like to add it to the database? (yes/no)")
                while restart_loop:
                    restart = input(">> ")
                    if restart == "yes":
                        choice = 3
                        restart_loop = False
                        continue
                    elif restart == "no":
                        restart_loop = False
                    else:
                        print("Invalid input. Please enter yes or no.")

        elif choice == 2:     # Läs in fil med historik
            data = input("Enter filename: ")
            cars_dict = read_from_file(data)
            print("Database loaded from file.")
        
        elif choice == 3:     # Lägg till ny bil
            reg_loop = True
            while reg_loop:
                reg_num = input("Registration number of new car: ")
                if reg_num in cars_dict:
                    print("Car already exists in database. Please enter a new registration number.")
                else:
                    reg_loop = False

            owner = input("Owner of the car (firstname & lastname): ")
            while True:
                car_class = input("Car class (light, medium, heavy): ")
                if car_class not in ["light", "medium", "heavy"]:
                    print("Invalid class. Please enter light, medium, or heavy.")
                else:
                    break
            print("Adding car to database...")
            print(add_car(reg_num, owner, car_class))
            print(cars_dict)

        elif choice == 4:     # Parkeringshistorik & kostnader
            reg_num = input("Registration number of car to show history for: ")
            try:
                car = cars_dict[reg_num]
                search_car = Car(car["reg_num"], car["owner"], car["car_class"], car["balance"], car["parking_history"])
                search_car.show_parking()
            except KeyError:
                print(f"Car [{reg_num}] not found in database. Returning to main menu.")

        elif choice == 5:     # Betala parkering
            reg_num = input("Registration number of car to pay for: ")
            try:
                car = cars_dict[reg_num]
                parked_car = Car(car["reg_num"], car["owner"], car["car_class"], car["balance"], car["parking_history"])
                print(parked_car.pay_parking())
            except KeyError:
                print(f"Car [{reg_num}] not found in database. Returning to main menu.")
            
        elif choice == 6:     # Avsluta NOTE fixa utan break
            print('"Bye bye!" - Mario the Italian plumber')
            loop = False
            break

        elif choice == 0:
            car1 = Car("ABC123", "Someone", "light")
            
            parking1 = Parking("12:00", "14:30", car1.car_format()["car_class"])
            car1.add_parking(parking1)
            parking2 = Parking("16:23", "21:58", car1.car_format()["car_class"])
            car1.add_parking(parking2)

            cars_dict[car1.reg_num] = car1.car_format()
            print("\n" + str(car1) + "\n")
            car1.show_parking()

            write_to_file("data.json")
            # print(read_from_file("data.json"))
            # cars_dict = read_from_file("data.json")

            print("\n------------------------------------\n")

            print(car1.show_balance())

            print()

        print()
        choice = menu()
        print()

def main():
    execute(menu())

if __name__ == "__main__":
    main()

    # NOTE Varna användaren om parkering är misstänksamt lång, dvs. t.ex om det är över 24 timmar
    # NOTE Lägga till så alla bilar i listan & i filer konverteras till Car-klassen.