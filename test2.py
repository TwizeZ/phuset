import time
import tkinter as tk
import json

class Person():
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance
        self.cars = []
    
    def __str__(self):
        cars_info = "\n".join(str(car) for car in self.cars)
        return f"Person: {self.name}, {self.balance}\n{cars_info}"
    
    def person_format(self):
        return {"name": self.name, "balance": self.balance, "cars": self.cars}

    def get_name(self):
        return self.name

    def deposit(self, amount):
        self.balance += amount

    def add_car(self, car):
        self.cars.append(car.car_format())

    def remove_car(self, reg_num):
        for car in self.cars:
            if car["reg_num"] == reg_num:
                self.cars.remove(car)
                return True
        return False
    
    def get_cost(self):
        cost = 0
        for car in self.cars:
            for parking in car["parking_history"]:
                cost += parking["total_cost"]
        return cost


class Car():
    def __init__(self, reg_num, car_type, owner):
        self.reg_num = reg_num
        self.car_type = car_type
        self.owner = owner
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


def main():
    # Just for testing
    person1 = Person("John Doe", -100)
    car1 = Car("ABC123", "Someone", "small")
    car2 = Car("DEF456", "Also Someone", "medium")
    car3 = Car("GHI789", "Another Someone", "large")
    
    person1.add_car(car1)
    person1.add_car(car2)
    person1.add_car(car3)
    print(person1)
    print(person1.get_name())

    parking1 = Parking(car1.car_format()["reg_num"], car1.car_format()["car_type"], 12, 15)
    parking2 = Parking(car1.car_format()["reg_num"], car1.car_format()["car_type"], 12, 16)
    car1.add_parking(parking1)
    car1.add_parking(parking2)

    print()
    print(person1.person_format())

    person1.remove_car("DEF456")

    print()
    print(person1.person_format())

    write_to_file(person1.person_format())

    print()
    print("Total cost:", person1.get_cost())

    print()
    persons = []
    persons.append(person1.person_format())
    print(persons)

if __name__ == "__main__":
    main()

    # NOTE Varna användaren om parkering är misstänksamt lång, dvs. t.ex om det är över 24 timmar