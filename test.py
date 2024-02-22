import time
import tkinter as tk
import json

class Person():
    def __init__(self, name, balance:int, cars = []):
        self.name = name
        self.balance = balance
        self.cars = cars
    
    def __str__(self):
        return f"Person: {self.name}, {self.cars}"
    
    def deposit(self, amount):
        self.balance += amount

class Car(Person):
    def __init__(self, registration_num, car_type):
        self.registration_num = registration_num
        self.car_type = car_type
    
    def __str__(self):
        return f"Car: {self.registration_num}, {self.owner}, {self.car_type}, {self.car_weight}"

def calc_car_type(car_weight):
    if car_weight < 1200:
        return "light"
    elif car_weight < 2000:
        return "medium"
    else:
        return "heavy"

def main():
    car1 = Car("ABC123", "John Doe", "Toyota", 1500)
    car2 = Car("DEF456", "Jane Doe", "Honda", 2500)
    car3 = Car("GHI789", "Jim Doe", "Ford", 3000)
    car4 = Car("JKL012", "Jill Doe", "Chevy", 1000)
    car5 = Car("MNO345", "Jack Doe", "Dodge", 2000)

    cars = [car1, car2, car3, car4, car5]

    for car in cars:
        print(car)
        print(f"The car is {calc_car_type(car.car_weight)}")

    root = tk.Tk()
    root.title("Car List")
    root.geometry("400x400")

    canvas = tk.Canvas(root, bg="white")
    canvas.pack(expand=True, fill="both")

    for i, car in enumerate(cars):
        canvas.create_text(200, 50 + i * 50, text=car, font=("Arial", 12))

    root.mainloop()

if __name__ == "__main__":
    main()


    # NOTE Varna användaren om parkering är misstänksamt lång, dvs. t.ex om det är över 24 timmar