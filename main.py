from datetime import datetime
from math import ceil
import json
import os
from inspect import getframeinfo, currentframe

cars_dict = {}  # The dictionary where all cars and their information are stored
DATAFILE = "data.json"  # The file where the data is automatically saved


class Car:
    """
    Attributes:

    reg_num: The registration number of the car.
    owner: The owner of the car.
    car_class: The car's weight class. Can be light, medium, or heavy.
    balance: The balance of the car's account.
    parking_history: A list of all parking's the car has made.
    """

    def __init__(self, reg_num, owner, car_class, balance=0, parking_history=[]):
        """
        :param reg_num: The registration number of the car.
        :param owner: The owner of the car.
        :param car_class: The car's weight class. Can be light, medium, or heavy.
        :param balance: The balance of the car's account.
        :param parking_history: A list of all parking's the car has made.
        """
        self.reg_num = reg_num.upper()
        self.owner = owner
        self.car_class = car_class
        self.balance = balance
        self.parking_history = parking_history

    def __str__(self):
        """Car information for printouts.

        :return: A formatted string containing the car's information.
        """
        return (f"Information about [{self.reg_num}]:"
                f"\n┗━ Owner: {self.owner}"
                f"\n┗━ Class: {self.car_class}"
                f"\n┗━ Balance: {self.balance}\n")

    def car_format(self):
        """Format used to save the car's information to the file.

        :return: A dictionary containing the car's information.
        """
        return {
            "reg_num": self.reg_num,
            "owner": self.owner,
            "car_class": self.car_class,
            "balance": self.balance,
            "parking_history": self.parking_history,
        }

    def new_parking(self, start_time, end_time):
        """Registers a new parking for the car.

        :param start_time: The time the parking starts.
        :param end_time: The time the parking ends.

        :return: A confirmation message with the parking details.
        """
        parking = Parking(start_time, end_time, self.car_class)
        self.parking_history.append(parking.parking_format())
        cars_dict[self.reg_num] = self.car_format()

        return f"Parking confirmed. Details below:\n{parking}"

    def print_parking(self):
        """Prints the parking history for the car.

        :return: A formatted string containing the car's parking history, or False if no parking's have been made.
        """
        parking_history = self.parking_history
        if not parking_history:
            return False
        else:
            summary = f"Parking history for [{self.reg_num}]:"
            for i, parking in enumerate(self.parking_history):
                current_parking = Parking(
                    parking["start_time"],
                    parking["end_time"],
                    self.car_class,
                    parking["paid"],
                    parking["date"],
                )
                summary += f"\n\nParking [{i + 1}]:\n{current_parking}"
            return summary

    def pay_parking(self, park_num):
        """Pays for a parking entry.

        :param park_num: The number of which parking entry to pay for.

        :return: A confirmation message with the new balance.
        """
        self.parking_history[park_num]["paid"] = True
        cars_dict[self.reg_num] = self.car_format()
        return f"Payment completed. New balance: {self.balance}. Thank you!"


class Parking:
    """
    Attributes:

    start_time: The parking's start time
    end_time: The parking's end time
    car_class: The car's weight class. Can be light, medium, or heavy.
    date: The date of the parking
    paid: If the parking has been paid for
    total_time: The total time the car was parked
    cost: The total cost of the parking
    """

    def __init__(
        self,
        start_time,
        end_time,
        car_class,
        paid=False,
        date=(str(datetime.now().date())),
    ):
        self.start_time = start_time
        self.end_time = end_time
        self.car_class = car_class
        self.date = date
        self.paid = paid
        self.total_time = self.calc_time()
        self.cost = self.calc_cost()

    def __str__(self):
        """Parking information for printouts.

        :return: A formatted string containing the parking's information.
        """
        return (f"┗━ Date: {self.date}\n"
                f"┗━ Time: {self.start_time} - {self.end_time} ({self.total_time})\n"
                f"┗━ Cost: {self.cost}\n"
                f"┗━ Paid: {self.paid}")

    def parking_format(self):
        """Format used to save the parking's information to the file.

        :return: A dictionary containing the parking's information.
        """
        return {
            "date": self.date,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "total_time": self.total_time,
            "cost": self.cost,
            "paid": self.paid,
        }

    def calc_time(self):
        """Calculates the total time the car was parked.

        :return: A string containing the total time.
        """
        year, month, day = str(self.date).split("-")

        start_hour, start_min = self.start_time.split(":")
        end_hour, end_min = self.end_time.split(":")

        ts1 = datetime(int(year), int(month), int(day), int(start_hour), int(start_min))
        ts2 = datetime(int(year), int(month), int(day), int(end_hour), int(end_min))

        total_time = ts2 - ts1

        return str(total_time)

    def calc_cost(self):
        """Calculates the cost of the parking.

        :return: The total cost of the parking.
        """
        hour, minute, _ = self.total_time.split(":")

        time = int(hour) + int(minute) / 60
        rounded_time = ceil(time * 2) / 2

        if self.car_class == "light":
            cost_per_hour = 15
        elif self.car_class == "medium":
            cost_per_hour = 20
        else:
            cost_per_hour = 25

        return round(cost_per_hour * rounded_time)  # Round up to avoid decimals


def write_to_file(datafile):
    """Writes all information in cars_dict to a file.

    :param datafile: The file to write to.

    :return: A confirmation message.
    """
    with open(datafile, "w", encoding="utf8") as file:
        json.dump(cars_dict, file, indent=4)
    return f"Data has been saved to file '{datafile}'."


def read_from_file(datafile):
    """Reads all information from a file and loads it into cars_dict.

    :param datafile: The file to read from.

    :return: A confirmation message.
    """
    try:
        if os.stat(datafile).st_size == 0:  # If file is empty
            raise TypeError
        else:
            with open(datafile, "r", encoding="utf8") as file:
                loaded_data = json.load(file)
                for reg_num, car_data in loaded_data.items():
                    cars_dict[reg_num] = car_data

            return f"Loaded {len(loaded_data)} entities from file."
    except FileNotFoundError:
        return "\nFile not found. Please try another file."
    except TypeError:
        return "\nFile is empty. Please try again."
    except json.decoder.JSONDecodeError:  # If file is not a JSON-file
        return "\nInvalid file format. No data was imported. Make sure to input a JSON-file."
    except Exception as e:  # If any other error occurs in the function
        return f"An error occurred: {e}\nError occurred on line {getframeinfo(currentframe()).lineno}"


def int_input(prompt):
    """Asks the user for an integer input.

    :param prompt: The message to display to the user.

    :return: The user's input if it's an integer.
    """
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a number.")
        except Exception as e:  # If any other error occurs in the function
            print(f"An error occurred: {e}")
            print(f"Error occurred on line {getframeinfo(currentframe()).lineno}")
            continue


def time_input(prompt):
    """Asks the user for a time input in the format HH:MM.

    :param prompt: The message to display to the user.

    :return: The user's input if it's a valid time.
    """
    while True:
        try:
            time = input(prompt)
            hours, minutes = time.split(":")
            if int(hours) in range(0, 24) and int(minutes) in range(0, 60):
                if time[0] == "0":  # Example: 09:00 -> 9:00
                    time = time[1:]
                return time
            else:
                raise ValueError
        except ValueError:
            print("Please follow the format HH:MM.")
        except Exception as e:  # If any other error occurs in the function
            print(f"An error occurred: {e}")
            print(f"Error occurred on line {getframeinfo(currentframe()).lineno}")
            continue


def reg_check(prompt):
    """Checks if the registration number exists in the database.

    :param prompt: The message to display to the user.

    :return: The car as a Car-class object if it exists in the database.
    """
    while True:
        try:
            reg_num = input(prompt).upper()
            car_info = cars_dict[reg_num]
            checked_car = Car(
                car_info["reg_num"],
                car_info["owner"],
                car_info["car_class"],
                car_info["balance"],
                car_info["parking_history"],
            )
            return checked_car
        except KeyError:
            print(
                f"Car [{reg_num}] not found in database. You can add a new car from the main menu."
            )
        except Exception as e:  # If any other error occurs in the function
            print(f"An error occurred: {e}")
            print(f"Error occurred on line {getframeinfo(currentframe()).lineno}")
            continue


def new_car(reg_num, owner, car_class):
    """Creates a new car and adds it to cars_dict.

    :param reg_num: The registration number of the car.
    :param owner: The owner of the car.
    :param car_class: The car's weight class. Can be light, medium, or heavy.
    """
    car = Car(reg_num, owner, car_class)
    cars_dict[car.reg_num] = car.car_format()
    return f"Car [{reg_num}] was added to database.\n\n{car}"


def menu():
    """Main menu string for the program.

    :return: The user's choice.
    """
    print(
        """
            Park Dark Mark Bark
-------------------------------------------
{1} New parking
{2} Read file & history
{3} Add new car
{4} Parking history & costs
{5} Pay for parking
{6} Display car information
{7} Exit
          """
    )

    menu_loop = True
    while menu_loop:
        choice = int_input(">> ")
        if choice in range(1, 8):
            return choice
        else:
            print("Invalid input. Please try again.")


def execute(choice, db_dict=cars_dict):
    """Executes the user's choice from the main menu.

    :param choice: The user's choice.
    :param db_dict: The dictionary where all cars and their information are stored.
    """
    while True:
        if choice == 1:  # New parking
            car = reg_check("Registration number: ")
            start_time = time_input("Start time (HH:MM): ")

            while True:
                end_time = time_input("End time (HH:MM): ")

                start_h, start_m = (int(t) for t in start_time.split(":"))
                end_h, end_m = (int(t) for t in end_time.split(":"))

                if (
                    end_h < start_h
                    or (end_h <= start_h and end_m < start_m)
                    or (end_h == start_h and end_m == start_m)
                ):
                    print("End time must be a later time than start time.")
                    print(
                        "If you'd like to park over midnight, please make two separate parking's."
                    )
                else:
                    break

            print()
            print(car.new_parking(start_time, end_time))

        elif choice == 2:  # Read file & history
            data = input("Enter filename: ")
            print(read_from_file(data))

        elif choice == 3:  # Add new car
            new_car_loop = True
            while new_car_loop:
                reg_num = input("Registration number of new car: ").upper()
                if reg_num == "":
                    print("Registration number cannot be empty.")
                elif reg_num in db_dict:
                    print(
                        "Car already exists in database. Please enter a new registration number."
                    )
                else:
                    new_car_loop = False

            owner_loop = True
            while owner_loop:
                owner = input("Owner of the car: ").title()
                if owner == "":
                    print("Owner cannot be empty.")
                else:
                    owner_loop = False

            car_class_loop = True
            while car_class_loop:
                car_class = input("Car class (light, medium, heavy): ")
                if car_class not in ["light", "medium", "heavy"]:
                    print("Invalid class. Please enter light, medium, or heavy.")
                else:
                    car_class_loop = False

            print("\nAdding car to database...")
            print(new_car(reg_num, owner, car_class))

        elif choice == 4:  # Parking history & costs
            car = reg_check("Registration number of car to show history for: ")
            parking_info = car.print_parking()
            if not parking_info:
                print(f"\nNo parking's has been registered for [{car.reg_num}].")
                continue
            else:
                print(parking_info)

        elif choice == 5:  # Pay for parking
            car = reg_check("Registration number of car to pay for: ")
            parking_info = car.print_parking()
            if not parking_info:
                print(f"\nNo parking's has been registered for [{car.reg_num}].")
                continue
            else:
                print(parking_info)

            pay_loop = True
            while pay_loop:
                park_num = (
                    int_input(f"\nWhich parking entry would you like to pay for?\n>> ")
                    - 1
                )
                try:
                    if park_num < 0:
                        raise IndexError
                    elif car.parking_history[park_num]["paid"]:
                        print("This parking has already been paid for.")
                    else:
                        cost = car.parking_history[park_num]["cost"]
                        print(f"\nThe cost for the parking is {cost}.")
                        pay_loop = False
                except IndexError:
                    print("That is not an option.")
                except Exception as e:  # If any other error occurs in the function
                    print(f"An error occurred: {e}")
                    print(
                        f"Error occurred on line {getframeinfo(currentframe()).lineno}"
                    )
                    continue

            if car.balance != 0:  # Only triggers if the car has a previous balance
                balance_loop = True
                while balance_loop:
                    use_balance = input(
                        "Would you like to use your balance to pay for the parking? (yes/no)\n>> "
                    )
                    print()
                    if use_balance.lower() == "yes":
                        if car.balance == cost:
                            cost, car.balance = 0, 0
                        elif car.balance < cost:
                            cost -= car.balance
                            print(f"Payment of {car.balance} was made. {cost} remains.")
                            car.balance = 0
                        else:
                            car.balance -= cost
                        balance_loop = False
                    elif use_balance.lower() == "no":
                        balance_loop = False
                    else:
                        print("Invalid input. Please enter yes or no.")

            if cost != 0:  # Only triggers if the parking has not been fully paid
                payment_loop = True
                while payment_loop:
                    payment = int_input(
                        f"\nHow much would you like to pay? (minimum {cost})"
                        f"\n(If you pay more than the parking's fine, it will be added to a total balance.)\n>> "
                    )
                    print()
                    if payment < cost:
                        print(f"Not enough money. At least {cost} is required.")
                    else:
                        car.balance = car.balance + (payment - cost)
                        payment_loop = False

            print(car.pay_parking(park_num))

        elif choice == 6:  # Display car information
            car = reg_check("Registration number of car to display information for: ")
            print("\n" + str(car))

        elif choice == 7:  # Exit
            break

        print()
        choice = menu()  # Loop back to the main menu
        print()


def main():
    """Main function for the program."""
    os.system(
        "cls" if os.name == "nt" else "clear"
    )  # Clears the terminal before starting
    print(read_from_file(DATAFILE))  # Reads the data from the file
    execute(menu())  # Executes the main menu and runs the program
    print("\nSaving to file...")
    print(write_to_file(DATAFILE))  # Writes the data to the file


if __name__ == "__main__":
    main()
