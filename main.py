from datetime import datetime
import json

DATABASE = "data.json"
cars_list = []

class Car():
    def __init__(self, reg_num, owner, car_class):
        self.reg_num = reg_num
        self.owner = owner
        self.car_class = car_class
        self.parking_history = []
    
    def __str__(self):
        return f"Car info: {self.reg_num}, {self.car_class}."
    
    def car_format(self):
        return {"reg_num": self.reg_num, "owner": self.owner, "car_class": self.car_class, "parking_history": self.parking_history}
    
    def show_debt(self):
        pass
    
class Parking():
    def __init__(self, start_time, end_time, car_class):
        self.start_time = start_time
        self.end_time = end_time
        self.car_class = car_class
        self.total_time = end_time - start_time
        self.total_cost = self.calc_cost()
    
    def __str__(self):
        return f"Total time: {self.total_time}, Total cost: {self.total_cost}"
    
    def parking_format(self):
        return {"start_time": self.start_time, "end_time": self.end_time, "total_time": self.total_time, "total_cost": self.total_cost}

    def calc_cost(self):
        if self.car_class == "light":
            cost_per_hour = 15
        elif self.car_class == "medium":
            cost_per_hour = 20
        else:
            cost_per_hour = 25
        
        return cost_per_hour * self.total_time          # NOTE: avrunda pris uppåt till närmaste halvtimme. Måste förstå hur det kan göras med tid

def write_to_file(data):
    with open(DATABASE, "w") as file:
        json.dump(data, file, indent=4)

def read_from_file():
    with open("data.json", "r") as file:
        data = json.load(file)
    return data

def int_input(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a number.")

def pay_parking():
    print("ALL PARKINGS FOR A CAR HERE")
    print("Which parking do you want to pay for?")
    print("How much do you want to pay?")

def add_car(reg_num, owner, car_class):
    pass

def remove_car(reg_num):                                # NOTE Ska bara kunna göras om inga kostnader finns kvar att betala
    pass


def main():
    # Just for testing
    car1 = Car("ABC123", "Someone", "small")
    car2 = Car("DEF456", "Also Someone", "medium")
    car3 = Car("GHI789", "Another Someone", "large")

    parking1 = Parking(12, 15, car1.car_format()["car_class"])
    car1.add_parking(parking1)
    parking2 = Parking(12, 15, car1.car_format()["car_class"])
    car2.add_parking(parking2)

    cars_list.append(car1.car_format())
    cars_list.append(car2.car_format())

    print(car1.car_format())

    print()

    write_to_file(cars_list)

    print(read_from_file())

    print("------------------------------------")

    # print(Car.show_balance())

    print()

if __name__ == "__main__":
    main()

    # NOTE Varna användaren om parkering är misstänksamt lång, dvs. t.ex om det är över 24 timmar