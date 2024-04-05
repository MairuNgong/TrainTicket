import tkinter as tk
import ttkbootstrap as ttk
from datetime import datetime
import requests
from ttkbootstrap.constants import *
import json

class MyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ticket Reservation System")
        self.cache = {
            "user" : None,
            "train_id" : None,
            "bogie_id" : None,
            "reservation_id" : None,
            "departure" : None,
            "destination" : None,
            "departure_time" : None,
            "destination_time" : None,
            "date" : None,
            "amount" : None
        }
        self.root.geometry("1200x600")

        self.main_page = ttk.Frame(root, width=1200, height=600)
        self.login_page = ttk.Frame(root, width=1000, height=600)
        self.register_page = ttk.Frame(root, width=1000, height=600)
        
        self.route_page = ttk.Frame(root, width=1200, height=600)
        self.trains_page = ttk.Frame(root, width=1000, height=600)
        self.bogies_page = ttk.Frame(root, width=1000, height=600)

        self.create_widgets_main()

        self.show_main()
        
    def create_widgets_main(self) :
        custom_font = ("Helvetica", 30)
        div_main_frame = ttk.Frame(self.main_page,)
        div_main_frame.pack()
        
        header_frame = ttk.Frame(div_main_frame, width=1200, height=200)
        header_frame.grid(row=0, pady=20)
        
        header_label = ttk.Label(
        header_frame,
        bootstyle="info",
        text="TRAIN TICKET RESERVATION",
        font=custom_font,
        )
        header_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        main_menu_frame = ttk.Frame(div_main_frame)
        main_menu_frame.grid(row=1)
        
        to_reservation_button = ttk.Button(main_menu_frame, bootstyle="success", text="RESERVATION", width=20, command=self.show_route)
        to_reservation_button.grid(row=0, padx=10, pady=10)
        
        to_login_button = ttk.Button(main_menu_frame, bootstyle="primary", text="LOGIN", width=20, command=self.show_login)
        to_login_button.grid(row=1, padx=10,pady=10)
        
        to_register_button = ttk.Button(main_menu_frame, bootstyle="primary-outline", text="REGISTER", width=20, command=self.show_register)
        to_register_button.grid(row=2, padx=10,pady=10)
        
    def create_widget_login(self) :
        #For when return to this page, clear the old one first
        for widget in self.login_page.winfo_children():
            widget.destroy()

        custom_font = ("Helvetica", 30)
        div_login_frame = ttk.Frame(self.login_page, width=1000, height=600)
        div_login_frame.pack()

        header_frame = ttk.Frame(div_login_frame, width=1000, height=100)
        header_frame.grid(row=0, pady=70)
        
        header_label = ttk.Label(
        header_frame,
        bootstyle="info",
        text="LOGIN",
        font=custom_font,
        )
        header_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        login_form = ttk.Frame(div_login_frame)
        login_form.grid(row=1)
        
        username_lebel = ttk.Label(login_form, text="USERNAME: ")
        username_lebel.grid(row=0, pady=10)
        
        username_Entry = ttk.Entry(login_form, width=20)
        username_Entry.grid(row=1, pady=10)
        
        password_lebel = ttk.Label(login_form, text="PASSWORD: ")
        password_lebel.grid(row=3, pady=10)
        
        password_Entry = ttk.Entry(login_form, width=20)
        password_Entry.grid(row=4, pady=10)

        error_label = ttk.Label(login_form, text="", foreground="red")
        error_label.grid(row=4, columnspan=2)
        
        login_button = ttk.Button(div_login_frame, text="Login", command= lambda : self.submit_login(username_Entry, password_Entry,error_label))
        login_button.grid(row=2, pady=20)
        
        back_button = ttk.Button(div_login_frame, bootstyle="info", text="go back", command=self.show_main)
        back_button.grid(row=3,pady=20, padx=20, sticky=tk.W)
        
    def create_widget_register(self) :
        #For when return to this page, clear the old one first
        for widget in self.register_page.winfo_children():
            widget.destroy()
        custom_font = ("Helvetica", 30)
        div_register_frame = ttk.Frame(self.register_page, width=1000, height=600)
        div_register_frame.pack()

        header_frame = ttk.Frame(div_register_frame, width=1000, height=100)
        header_frame.grid(row=0, pady=70)
        
        header_label = ttk.Label(
        header_frame,
        bootstyle="info",
        text="REGISTER",
        font=custom_font,
        )
        header_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        register_form = ttk.Frame(div_register_frame)
        register_form.grid(row=1)
        
        name_lebel = ttk.Label(register_form, text="NAME: ")
        name_lebel.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        
        name_Entry = ttk.Entry(register_form, width=20)
        name_Entry.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)
        
        username_lebel = ttk.Label(register_form, text="USERNAME: ")
        username_lebel.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        
        username_Entry = ttk.Entry(register_form, width=20)
        username_Entry.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)
        
        password_lebel = ttk.Label(register_form, text="PASSWORD: ")
        password_lebel.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        
        password_Entry = ttk.Entry(register_form, width=20)
        password_Entry.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)
        
        confirm_password_lebel = ttk.Label(register_form, text="CONFIRM PASSWORD: ")
        confirm_password_lebel.grid(row=3, column=0, pady=10)
        
        confirm_password_Entry = ttk.Entry(register_form, width=20)
        confirm_password_Entry.grid(row=3, column=1, pady=10)

        error_label = ttk.Label(register_form, text="", foreground="red")
        error_label.grid(row=4, columnspan=2)


        login_button = ttk.Button(div_register_frame, text="register", command=lambda : self.submit_register(username_Entry, name_Entry, password_Entry, confirm_password_Entry,error_label))
        login_button.grid(row=2, pady=20)
        
        back_button = ttk.Button(div_register_frame, bootstyle="info", text="go back", command=self.show_main)
        back_button.grid(row=3,pady=20, padx=20, sticky=tk.W)
    
    def create_widgets_route(self):
        for widget in self.route_page.winfo_children():
            widget.destroy()
        element_theme = "success"
        stations_list = MyApp.request_all_route_list()
        custom_font = ("Helvetica", 30)

        div_frame = ttk.Frame(self.route_page, width=1000, height=600)
        div_frame.pack()

        header_frame = ttk.Frame(div_frame, width=1000, height=100)
        header_frame.grid(row=0, pady=70)

        header_label = ttk.Label(
            header_frame,
            bootstyle="info",
            text="Train Ticket Reservation System",
            font=custom_font,
        )
        header_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        form_frame = ttk.Labelframe(
            div_frame, text="select route", bootstyle="primary", width=1000, height=400
        )
        form_frame.grid(row=1)

        label_departure = ttk.Label(
            form_frame, bootstyle=element_theme, text="Departure:"
        )
        label_departure.grid(row=0, column=0, padx=10, pady=5)
        combo_departure = ttk.Combobox(
            form_frame,
            bootstyle=element_theme,
            values=[station["station name"] for station in stations_list],
        )
        combo_departure.grid(row=0, column=1, padx=10, pady=5)

        label_destination = ttk.Label(
            form_frame, bootstyle=element_theme, text="Destination:"
        )
        label_destination.grid(row=0, column=2, padx=10, pady=5)
        combo_destination = ttk.Combobox(
            form_frame,
            bootstyle=element_theme,
            values=[station["station name"] for station in stations_list],
        )
        combo_destination.grid(row=0, column=3, padx=10, pady=5)

        label_date = ttk.Label(form_frame, bootstyle=element_theme, text="Choose Date:")
        label_date.grid(row=0, column=4, padx=10, pady=5)
        my_date = ttk.DateEntry(form_frame, bootstyle=element_theme, width=12)
        my_date.grid(row=0, column=5, padx=10, pady=5)

        label_amount = ttk.Label(form_frame, bootstyle=element_theme, text="Amount:")
        label_amount.grid(row=0, column=6, padx=10, pady=5)
        entry_amount = ttk.Entry(form_frame, bootstyle=element_theme, width=5)
        entry_amount.grid(row=0, column=7, padx=5, pady=5)

        submit_button = ttk.Button(
            form_frame,
            bootstyle=element_theme,
            text="Submit",
            command=lambda: self.submit_req_route(
                combo_departure, combo_destination, my_date, entry_amount
            ),
        )
        submit_button.grid(row=0, column=8, padx=5, pady=10)

    def create_user_info_frame(self, target) :
        
        user_frame = ttk.LabelFrame(target, text="USER INFO", bootstyle="info", width=350, height=120) 
        user_frame.place(relx=0.7, rely=0.78)
        
        name_label = ttk.Label(user_frame, bootstyle="inverse-info", text="Name :")
        name_label.grid(row=0, column=0, padx=5, pady=5)
        
        username_label = ttk.Label(user_frame, bootstyle="dark", text=f"{self.cache["user"]["name"]}", width=20)
        username_label.grid(row=0, column=2, columnspan=2, padx=5, pady=5)
        
        to_ticket_list_button = ttk.Button(user_frame, bootstyle="primary", text="see ticket")
        to_ticket_list_button.grid(row=1, column=0, padx=5, pady=5)
        
        logout_button = ttk.Button(user_frame, bootstyle="primary", text="logout")
        logout_button.grid(row=1, column=2, padx=5, pady=5) 

    def create_widgets_show_trains(self, route_list):

        for index, route in enumerate(route_list):

            route_label = ttk.Label(self.trains_page, text=f"Route {index + 1}:", bootstyle=SUCCESS)
            route_label.grid(row=index, column=0, padx=10, pady=5, sticky="w")
            for train_id in route.keys():
                route_info = list(route.values())[0]
                departure = route_info["departure"]
                departure_time = route_info["departure_time"]
                destination = route_info["destination"]
                destination_time = route_info["destination_time"]

                train_id_label = tk.Label(self.trains_page, text=f"Train ID: {train_id}")
                train_id_label.grid(row=index, column=1, padx=10, pady=5, sticky="w")

                departure_label = tk.Label(self.trains_page, text=f"Departure: {departure}")
                departure_label.grid(row=index, column=2, padx=10, pady=5, sticky="w")

                departure_time_label = tk.Label(self.trains_page, text=f"Departure Time: {departure_time}")
                departure_time_label.grid(row=index, column=3, padx=10, pady=5, sticky="w")

                destination_label = tk.Label(self.trains_page, text=f"Destination: {destination}")
                destination_label.grid(row=index, column=4, padx=10, pady=5, sticky="w")

                destination_time_label = tk.Label(self.trains_page, text=f"Destination Time: {destination_time}")
                destination_time_label.grid(row=index, column=5, padx=10, pady=5, sticky="w")

                select_button = tk.Button(self.trains_page,text="Select",command=lambda train_id=train_id,departure_time=departure_time,destination_time=destination_time : self.submit_req_train(train_id,departure_time,destination_time))
                select_button.grid(row=index, column=len(route_info) + 1, padx=10, pady=5)

        button = tk.Button(self.trains_page, text="Go Back", command=self.show_route)
        button.grid(row=len(route_list), column=0, pady=10)

    def create_widgets_show_bogies(self, bogie_list):
        for widget in self.bogies_page.winfo_children():
            widget.destroy()

        for index, bogie in enumerate(bogie_list):
            for bogie_id in bogie.keys():
                bogie_label = tk.Label(self.bogies_page, text=f"{bogie_id}")
                bogie_label.grid(row=index, column=0, padx=10, pady=5)

        button = tk.Button(self.bogies_page, text="Go Back", command=self.show_trains)
        button.grid(row=len(bogie_list), column=0, pady=10)

        
    def create_widgets_show_seat(self):
        pass
    
    def submit_login(self, username_Entry, password_Entry, error_label):
        username = username_Entry.get()
        password = password_Entry.get()
        response = MyApp.fetch_login(username, password)
        if response == "Wrong Password or No Username":
            error_label.config(text="Wrong Password or No Username", foreground="red")
        else:
            print(response)
            self.cache["user"] = response
            self.create_user_info_frame(self.main_page)
            self.show_main()
    def submit_register(self, username_Entry, name_Entry, password_Entry, confirm_password_Entry,error_label):
        username = username_Entry.get()
        name = name_Entry.get()
        password = password_Entry.get()
        confirm_password = confirm_password_Entry.get()

        if password != confirm_password:
            error_label.config(text="Passwords do not match")
        else :
            response = MyApp.fetch_register(username,name,password)
            if response == "Successful":
                error_label.config(text="Successful",foreground="green")
            elif response == "Username already exists.":
                error_label.config(text="Username already exists.",foreground="red")


    def submit_req_route(
        self, combo_departure, combo_destination, my_date, entry_amount
    ):
        result_route_list = MyApp.fetch_choose_route(
            combo_departure, combo_destination, my_date, entry_amount
        )
        self.create_widgets_show_trains(result_route_list)
        self.cache["departure"] = combo_departure
        self.cache["destination"] = combo_destination
        self.cache["date"] = my_date
        self.cache["amount"] = entry_amount
        self.show_trains()

    def submit_req_train(self, train_id,departure_time,destination_time):
        result_bogie_list = MyApp.fetch_choose_train(train_id)
        self.create_widgets_show_bogies(result_bogie_list)
        self.cache["train_id"] = train_id
        self.cache["departure_time"] = departure_time
        self.cache["destination_time"] = destination_time
        self.show_bogies()
        
    @staticmethod
    def fetch_register(username, name, password):
        form = {"username":username, "name":name, "password":password}
        response = requests.post(
            "http://localhost:8000/register",data=json.dumps(form))
        result_response = response.json()
        
        return result_response
    @staticmethod
    def fetch_login(username, password):
        form = {"username":username, "password":password}
        response = requests.get(
            "http://localhost:8000/login",data=json.dumps(form))
        result_response = response.json()
        return result_response

    @staticmethod
    def fetch_choose_route(combo_departure, combo_destination, my_date, entry_amount):
        departure = combo_departure.get()
        destination = combo_destination.get()
        choose_date = my_date.entry.get()
        amount = entry_amount.get()

        choose_date = datetime.strptime(choose_date, "%m/%d/%Y")

        choose_date = choose_date.strftime("%Y-%m-%d")

        response = requests.get(
            "http://localhost:8000/route",
            params={
                "departure": departure,
                "destination": destination,
                "choose_date": choose_date,
                "amount": amount,
            },
        )
        result_route_list = response.json()
        return result_route_list

    @staticmethod
    def fetch_choose_train(train_id):
        train_id = train_id

        response = requests.get(
            "http://localhost:8000/train",
            params={
                "train_id": train_id,
            },
        )
        result_train_list = response.json()
        return result_train_list

    @staticmethod
    def request_all_route_list():
        try:
            response = requests.get("http://localhost:8000/root")
            if response.status_code == 200:
                stations_list = response.json()
                return stations_list
            else:
                print("Failed to fetch station data")
        except Exception as e:
            print("Error fetching station data:", e)


    def show_main(self) :
        self.main_page.pack(fill=tk.BOTH, expand=True)
        self.login_page.pack_forget()
        self.register_page.pack_forget()
        self.route_page.pack_forget()
        self.trains_page.pack_forget()
        self.bogies_page.pack_forget()
    
    def show_login(self) :
        self.create_widget_login()
        self.main_page.pack_forget()
        self.register_page.pack_forget()
        self.route_page.pack_forget()
        self.trains_page.pack_forget()
        self.bogies_page.pack_forget()
        self.login_page.pack()
        
    def show_register(self) :
        self.create_widget_register()
        self.main_page.pack_forget()
        self.login_page.pack_forget()
        self.route_page.pack_forget()
        self.trains_page.pack_forget()
        self.bogies_page.pack_forget()
        self.register_page.pack()
        
    def show_route(self):
        self.create_widgets_route()
        self.main_page.pack_forget()
        self.login_page.pack_forget()
        self.register_page.pack_forget()
        self.route_page.pack()
        self.trains_page.pack_forget()
        self.bogies_page.pack_forget()
        
    def show_trains(self):
        self.main_page.pack_forget()
        self.login_page.pack_forget()
        self.register_page.pack_forget()
        self.route_page.pack_forget()
        self.trains_page.pack()
        self.bogies_page.pack_forget()

    def show_bogies(self):
        self.main_page.pack_forget()
        self.login_page.pack_forget()
        self.register_page.pack_forget()
        self.route_page.pack_forget()
        self.trains_page.pack_forget()
        self.bogies_page.pack()

if __name__ == "__main__":
    root = ttk.Window(themename="minty")
    app = MyApp(root)
    root.mainloop()
