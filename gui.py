import tkinter as tk
from tkinter import *
import main


class Application(Frame):
    """Main GUI class for the program.

    :param Frame: tkinter Frame class
    """

    def __init__(self, master):
        """Initializes the GUI.

        :param master: tkinter root
        """
        Frame.__init__(self, master)
        self.grid()
        self.homescreen()

    def homescreen(self):
        """Creates the main menu screen.
        """
        Label(self,
              text="Registration Number // File name:"
              ).grid(row=0, column=0, sticky=W)
        self.reg_num_ent = Entry(self)
        self.reg_num_ent.grid(row=0, column=1, sticky=W)

        Button(self,
               text="Read from file",
               command=self.bttn_read_from_file
               ).grid(row=0, column=3, sticky=W)

        Button(self,
               text="Display car info",
               command=self.bttn_display_car
               ).grid(row=1, column=3, sticky=W)

        Button(self,
               text="Parking history & costs",
               command=self.bttn_parking_history
               ).grid(row=2, column=3, sticky=W)

        Label(self,
              text="‎"
              ).grid(row=3, column=3, sticky=W)

        Button(self,
               text="New Parking",
               command=self.new_parking_screen
               ).grid(row=4, column=3, sticky=W)

        Button(self,
               text="New Car",
               command=self.new_car_screen
               ).grid(row=5, column=3, sticky=W)

        Button(self,
               text="Pay Parking",
               command=self.pay_parking_screen
               ).grid(row=6, column=3, sticky=W)

        Button(self,
               text="Exit",
               command=root.destroy
               ).grid(row=7, column=3, sticky=W)

        Label(self,
              text="Outputs:"
              ).grid(row=7, column=0, sticky=W)

        self.output_txt = Text(self, width=55, height=10, wrap=WORD)
        self.output_txt.grid(row=8, column=0, columnspan=2)

    def new_car_screen(self):
        """Creates a new window for adding a new car.
        """
        # open a new window
        car_window = self.new_window()

        Label(car_window,
              text="Registration Number:"
              ).grid(row=0, column=0, sticky=W)
        car_window.new_reg_num_ent = Entry(car_window)
        car_window.new_reg_num_ent.grid(row=0, column=1, sticky=W)

        Label(car_window,
              text="Owner:"
              ).grid(row=1, column=0, sticky=W)
        car_window.owner_ent = Entry(car_window)
        car_window.owner_ent.grid(row=1, column=1, sticky=W)

        Label(car_window,
              text="Car Class:"
              ).grid(row=2, column=0, sticky=W)
        car_window.class_opt = OptionMenu(car_window, StringVar(car_window), "light", "medium", "heavy")
        car_window.class_opt.grid(row=2, column=1, sticky=W)

        car_window.bttn_add = Button(car_window,
                                     text="Add new car",
                                     command=lambda: self.bttn_new_car(car_window))
        car_window.bttn_add.grid(row=3, column=0, sticky=W)

    def new_parking_screen(self):
        """Creates a new window for adding a new parking.
        """
        # open a new window
        park_window = self.new_window()

        Label(park_window,
              text="Registration Number:"
              ).grid(row=0, column=0, sticky=W)
        park_window.parking_reg_num_ent = Entry(park_window)
        park_window.parking_reg_num_ent.grid(row=0, column=1, sticky=W)

        Label(park_window,
              text="Start time:"
              ).grid(row=1, column=0, sticky=W)
        park_window.parking_start_ent = Entry(park_window)
        park_window.parking_start_ent.grid(row=1, column=1, sticky=W)

        Label(park_window,
              text="End time:"
              ).grid(row=2, column=0, sticky=W)
        park_window.parking_end_ent = Entry(park_window)
        park_window.parking_end_ent.grid(row=2, column=1, sticky=W)

        park_window.bttn_add = Button(park_window,
                                      text="Add new parking",
                                      command=lambda: self.bttn_add_parking(park_window))
        park_window.bttn_add.grid(row=3, column=0, sticky=W)

    def pay_parking_screen(self):
        """Creates a new window for paying for a parking.
        """
        # open a new window
        pay_window = self.new_window()

        Label(pay_window,
              text="Registration Number:"
              ).grid(row=0, column=0, sticky=W)
        pay_window.pay_reg_num_ent = Entry(pay_window)
        pay_window.pay_reg_num_ent.grid(row=0, column=1, sticky=W)

        Label(pay_window,
              text="To know what parking to pay for, check the parking history before."
              ).grid(row=1, column=0, columnspan=2, sticky=W)

        Label(pay_window,
              text="Parking index number:"
              ).grid(row=2, column=0, sticky=W)
        pay_window.park_num_ent = Entry(pay_window)
        pay_window.park_num_ent.grid(row=2, column=1, sticky=W)

        pay_window.pay_with_bal = BooleanVar()
        Checkbutton(pay_window,
                    text="Pay with balance",
                    variable=pay_window.pay_with_bal
                    ).grid(row=3, column=1, sticky=W)

        Label(pay_window,
              text="Amount to pay:"
              ).grid(row=4, column=0, sticky=W)
        pay_window.pay_amount_ent = Entry(pay_window)
        pay_window.pay_amount_ent.grid(row=4, column=1, sticky=W)

        pay_window.bttn_add = Button(pay_window,
                                     text="Pay parking",
                                     command=lambda: self.bttn_pay_parking(pay_window))
        pay_window.bttn_add.grid(row=5, column=1, sticky=W)

        Label(pay_window,
              text="‎"
              ).grid(row=6, column=0, sticky=W)

        Label(pay_window,
              text="NOTE: When paying with balance, the cost of the parking will be deducted by the amount of balance."
              ).grid(row=7, column=0, columnspan=3, sticky=W)

        Label(pay_window,
              text="If the balance does not cover the cost, the remaining amount have to be paid in the second input."
              ).grid(row=8, column=0, columnspan=3, sticky=W)

        Label(pay_window,
              text="If the amount is higher than the cost of the parking, the additional funds will be added to the "
                   "balance."
              ).grid(row=9, column=0, columnspan=3, sticky=W)

    # Helper functions
    def new_output(self, prompt, del_window=None):
        """Clears the output field and inserts a new prompt.

        :param prompt: the input prompt
        :param del_window: tkinter window to be destroyed
        """
        self.output_txt.delete(0.0, END)
        self.output_txt.insert(0.0, prompt)
        if del_window:
            del_window.destroy()
    
    def new_window(self):
        """Creates a new window.

        :return: new_window
        """
        new_window = Toplevel(root)
        new_window.title("Screen")
        new_window.geometry("700x350")
        return new_window

    def reg_check(self, reg_num):
        """Checks if the registration number exists in the database.

        :param reg_num: the registration number to be checked

        :return: the car object if it exists, otherwise a string
        """
        try:
            car_obj = main.cars_dict[reg_num]
            checked_car = main.Car(car_obj["reg_num"],
                                   car_obj["owner"],
                                   car_obj["car_class"],
                                   car_obj["balance"],
                                   car_obj["parking_history"]
                                   )
            return checked_car
        except KeyError:
            return f"Car [{reg_num}] not found in database. You can add a new car from the main menu."

    def time_input(self, time):
        """Checks if the input time is in the correct format.

        :param time: the input time
        
        :return: the time, hours, and minutes if the input is correct, otherwise a string
        """
        try:
            hours, minutes = time.split(":")
            if int(hours) in range(0, 24) and int(minutes) in range(0, 60):
                if time[0] == "0":
                    time = time[1:]
                return time, hours, minutes
            else:
                raise ValueError
        except ValueError:
            return "Please follow the format HH:MM.", None, None

    # Button functions
    def bttn_read_from_file(self):
        """Reads the data from a JSON file.
        """
        filename = self.reg_num_ent.get()

        if filename == "":
            self.new_output("Please enter a file name in the input field.\nFormat: 'filename.json'.")
        else:
            file_info = main.read_from_file(filename)
            self.new_output(file_info)
            self.reg_num_ent.delete(0, 'end')

    def bttn_display_car(self):
        """Displays the car's information.
        """
        reg_num = self.reg_num_ent.get().upper()
        car_obj = self.reg_check(reg_num)
        if reg_num == "":
            self.new_output("Please enter a registration number in the input field.")
        elif not isinstance(car_obj, main.Car):
            self.new_output(car_obj)
        else:
            self.new_output(car_obj)

    def bttn_new_car(self, window):
        """Adds a new car to the database.

        :param window: new car window
        """
        reg_num = window.new_reg_num_ent.get().upper()
        owner = window.owner_ent.get().title()
        car_class = window.class_opt.cget("text")

        if reg_num == "" or owner == "" or car_class == "":
            self.new_output("All fields must be filled. Try again.", window)
        elif reg_num in main.cars_dict:
            self.new_output("Car already exists. Try again with another registration number.", window)
        else:
            car_obj = main.new_car(reg_num, owner, car_class)
            self.new_output(car_obj, window)

    def bttn_add_parking(self, window):
        """Adds a new parking to the database.

        :param window: new parking window
        """
        reg_num = window.parking_reg_num_ent.get().upper()
        car_obj = self.reg_check(reg_num)
        start_time, start_h, start_m = self.time_input(window.parking_start_ent.get())
        end_time, end_h, end_m = self.time_input(window.parking_end_ent.get())

        if reg_num == "" or start_time == "" or end_time == "":
            self.new_output("All fields must be filled. Try again.", window)
        elif not isinstance(car_obj, main.Car):
            self.new_output(f"Car [{reg_num}] not found in database. Try again.", window)
        elif not start_h or not end_h:
            self.new_output("Please follow the format HH:MM.", window)
        elif end_h < start_h or (end_h <= start_h and end_m < start_m) or (end_h == start_h and end_m == start_m):
            self.new_output(
                "End time must be later than start time.\nIf you'd like to park over midnight, make two separate "
                "parkings.",
                window)
        else:
            new_parking = car_obj.new_parking(start_time, end_time)
            self.new_output(new_parking, window)

    def bttn_parking_history(self):
        """Displays the parking history of the car.
        """
        reg_num = self.reg_num_ent.get().upper()
        car_obj = self.reg_check(reg_num)

        if reg_num == "":
            self.new_output("Please enter a registration number in the input field.")
        elif not isinstance(car_obj, main.Car):
            self.new_output(car_obj)
        else:
            parking_history = car_obj.print_parking()
            if parking_history == False:
                self.new_output(f"Car [{reg_num}] has no parking history.")
            else:
                self.new_output(parking_history)

    def bttn_pay_parking(self, window):
        """Pays for a parking.

        :param window: pay parking window
        """
        reg_num = window.pay_reg_num_ent.get().upper()
        car_obj = self.reg_check(reg_num)
        try:
            park_num = int(window.park_num_ent.get()) - 1
            amount = int(window.pay_amount_ent.get())
            pay_with_bal = window.pay_with_bal.get()

            if reg_num == "" or amount == "":
                self.new_output("All fields must be filled. Try again.", window)
            elif not isinstance(car_obj, main.Car):
                self.new_output(car_obj, window)
            elif park_num < 0:
                self.new_output("Parking number must be a positive integer. Try again.", window)
            elif car_obj.parking_history[park_num]["paid"]:
                self.new_output(f"Parking {park_num + 1} has already been paid for.", window)
            else:
                cost = car_obj.parking_history[park_num]["cost"]
                print(pay_with_bal)
                if pay_with_bal:
                    if car_obj.balance == cost:
                        cost, car_obj.balance = 0, 0
                    elif car_obj.balance < cost:
                        cost -= car_obj.balance
                        car_obj.balance = 0
                    else:
                        car_obj.balance -= cost

                if amount < cost:
                    self.new_output(f"Payment failed. Amount must be at least {cost}.", window)
                else:
                    car_obj.balance += int(amount) - cost

                    payment = car_obj.pay_parking(park_num)
                    self.new_output(payment, window)
        except IndexError:
            self.new_output(f"Parking {park_num} does not exist. Try again.", window)
        except ValueError:
            self.new_output("Parking index number and amount must be integers. Try again.", window)


main.read_from_file(main.DATAFILE)  # Reads information from the data file

root = Tk()  # Creates the main window
root.title("ParkPulse")
root.geometry("700x400")
my_app = Application(root)  # Creates the main application
root.mainloop()  # Starts the main loop

main.write_to_file(main.DATAFILE)  # Writes information to the data file
