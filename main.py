import time
import tkinter as tk
import json

DATABASE = "data.json"

class Car():
    def __init__(self, reg_num, owner, car_type):
        self.reg_num = reg_num
        self.owner = owner
        self.car_type = car_type
        self.parking_history = []
    
    def __str__(self):
        return f"Car info: {self.reg_num}, {self.car_type}."
    
    def car_format(self):
        return {"reg_num": self.reg_num, "owner": self.owner, "car_type": self.car_type, "parking_history": self.parking_history}
    
    def add_parking(self, parking):
        self.parking_history.append(parking.parking_format())
    
class Parking(Car):
    def __init__(self, reg_num, car_type, owner, start_time, end_time):
        super().__init__(reg_num, car_type, owner)                          # NOTE: Går det att ta bort owner?
        self.start_time = start_time
        self.end_time = end_time
        self.total_time = end_time - start_time
        self.total_cost = self.calc_cost()
    
    def __str__(self):
        return f"Total time: {self.total_time}, Total cost: {self.total_cost}"
    
    def parking_format(self):
        return {"start_time": self.start_time, "end_time": self.end_time, "total_time": self.total_time, "total_cost": self.total_cost}

    def calc_cost(self):
        if self.car_type == "light":
            cost_per_hour = 15
        elif self.car_type == "medium":
            cost_per_hour = 20
        else:
            cost_per_hour = 25
        
        return cost_per_hour * self.total_time          # NOTE: avrunda pris uppåt till närmaste halvtimme.


def write_to_file(data):
    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)

def load_from_file():
    with open("data.json", "r") as file:
        data = json.load(file)
    return data

def deposit(balance, amount):
    balance += amount

def add_car(cars_list, new_car):
    cars_list.append(new_car.car_format())

def remove_car(cars_list, reg_num):
    for car in cars_list:
        if cars_list["reg_num"] == reg_num:
            cars_list.remove(car)
            return True
    return False

def get_cost(cars_list):
    cost = 0
    for car in cars_list:
        for parking in car["parking_history"]:
            cost += parking["total_cost"]
    return cost


def main():
    # Just for testing
    car1 = Car("ABC123", "Someone", "small")
    car2 = Car("DEF456", "Also Someone", "medium")
    car3 = Car("GHI789", "Another Someone", "large")

    parking1 = Parking(car1.car_format()["reg_num"], car1.car_format()["car_type"], car1.car_format()["owner"], 12, 15)
    parking2 = Parking(car2.car_format()["reg_num"], car2.car_format()["car_type"], car2.car_format()["owner"], 10, 17)
    car1.add_parking(parking1)
    car2.add_parking(parking2)

    print(car1.car_format())

    print()

    write_to_file(car1.car_format())

    print(load_from_file())

    print()
    # print("Total cost:", get_cost([car1.car_format()]))

    # print()
    # persons = []
    # persons.append(person1.person_format())
    # print(persons)

if __name__ == "__main__":
    main()

    # NOTE Varna användaren om parkering är misstänksamt lång, dvs. t.ex om det är över 24 timmar