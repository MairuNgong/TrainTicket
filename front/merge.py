from typing import List
import tkinter as tk
import ttkbootstrap as ttk
from datetime import datetime
import requests
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
import json
from tkinter import *

class Pay_Page(ttk.Frame) :
    def __init__(self, frame_controller) :
        super().__init__(frame_controller)
        
        self.pack(expand=True, fill=tk.BOTH)

        self.controller = frame_controller
        self.create_widgets_pay()          
        
    def create_widgets_pay(self) :
        for widget in self.winfo_children(): widget.destroy()
        
        self.radio_var = tk.StringVar(value="")
        self.credit_pass_input = tk.StringVar(value="xxx-xxx-xxx")
        self.promptpay_input = tk.StringVar(value="xxx-xxx-xxx")
        self.cvc_input = tk.StringVar(value="xxx")
        self.balance_credit_input = tk.StringVar(value="xxx")
        self.balance_promptpay_input = tk.StringVar(value="xxx")
        
        custom_font = ("Helvetica", 30)
        info = ("Helvetica", 13)
        aleart = ("Helvetica", 15)
        
        header_frame = ttk.Frame(self, width=1200, height=200)
        header_frame.pack(pady=50)
        
        header_label = ttk.Label(header_frame, bootstyle="primary", text="Payment", font=custom_font)
        header_label.pack()
        
        if self.controller.cache["price"] < 0:
            self.controller.cache["price"] = 0
        balance_req_label = ttk.Label(self, bootstyle="info", text=f"Amount of money you need to pay: {self.controller.cache["price"]} baht", font=info)
        balance_req_label.pack(pady=20)
        
        menu_frame = ttk.LabelFrame(self, bootstyle="primary", text="Choose Payment Methode")
        menu_frame.pack()
        
        credit_radiobutton = ttk.Radiobutton(menu_frame,bootstyle="info-outline-toolbutton",  variable=self.radio_var, value="credit", text="Credit Card", command= self.switch_payment_methode)
        credit_radiobutton.grid(row=0, column=0, padx=15, pady=10)
       
        promptpay_radiobutton = ttk.Radiobutton(menu_frame, bootstyle="info-outline-toolbutton", variable=self.radio_var, value="promptpay", text="Promptpay", command= self.switch_payment_methode)
        promptpay_radiobutton.grid(row=0, column=1, padx=15, pady=10)
        
        price_label = ttk.Label(self)
        price_label.pack()
        
        form_frame = ttk.Frame(self)
        form_frame.pack()
        
        self.credit_frame = ttk.Frame(form_frame)
        
        credit_pass_lable = ttk.Label(self.credit_frame, text="Enter Credit Card ID")
        credit_pass_lable.grid(row=1, column=0, padx=10)
        
        credit_pass_entry = ttk.Entry(self.credit_frame, textvariable=self.credit_pass_input)
        credit_pass_entry.grid(row=2, column=0, padx=10)
        
        cvc_label = ttk.Label(self.credit_frame, text="Enter CVC")
        cvc_label.grid(row=1, column=1, padx=10)
        
        cvc_entry = ttk.Entry(self.credit_frame, textvariable=self.cvc_input)
        cvc_entry.grid(row=2, column=1, padx=10)
        
        balance_label = ttk.Label(self.credit_frame, text="balance")
        balance_label.grid(row=1, column=2, padx=10)
        
        balance_credit_entry = ttk.Entry(self.credit_frame, textvariable=self.balance_credit_input)
        balance_credit_entry.grid(row=2, column=2, padx=10)
        
        
        self.promptpay_frame = ttk.Frame(form_frame)
        
        promptpay_lable = ttk.Label(self.promptpay_frame, text="Phone No.")
        promptpay_lable.grid(row=1, column=0, padx=10)
        
        promptpay_entry = ttk.Entry(self.promptpay_frame, textvariable=self.promptpay_input)
        promptpay_entry.grid(row=2, column=0, padx=10)
        
        balance_label = ttk.Label(self.promptpay_frame, text="balance")
        balance_label.grid(row=1, column=1, padx=10)
        
        balance_promptpay_entry = ttk.Entry(self.promptpay_frame, textvariable=self.balance_promptpay_input)
        balance_promptpay_entry.grid(row=2, column=1, padx=10)
        
        self.info_label = ttk.Label(self, bootstyle="danger", text="", font=aleart)
        
        self.submit_button = ttk.Button(self, text="SUBMIT", command=self.send_payload_payment, width=15)
        
        payload_main_menu_button = {"go_to": "main"}
        self.back_to_main_button = ttk.Button(self, text="BACK TO MAIN MENU", bootstyle="success", width=20, command=lambda: self.controller.set_page_state(payload_main_menu_button))
        
        payload_back_button = {"go_to": "summation_from_pay"}
        self.back_button = ttk.Button(self, bootstyle="info", text="go back", command=lambda: self.controller.set_page_state(payload_back_button))
        self.back_button.place(x=10, y=500)
        
    def raise_main_menu_button(self) :
        self.back_to_main_button.pack()
        self.back_button.destroy()
    def drop_aleart(self) :
        self.info_label.pack_forget()
        
    def drop_submit_button(self) :
        self.submit_button.pack_forget()
        
    def raise_info_label_text_set(self, message, type) :
        self.info_label.config(text=message)
        self.info_label.config(bootstyle=type)
        self.info_label.pack(pady=10)
        
    
    def switch_payment_methode(self) :
        
        if self.radio_var.get() == "credit" : 

            self.credit_frame.pack()
            self.promptpay_frame.pack_forget()
            self.submit_button.pack(pady=10)
        elif self.radio_var.get() == "promptpay" :

            self.promptpay_frame.pack()
            self.credit_frame.pack_forget()
            self.submit_button.pack(pady=10)
            
    def validate_balance(self, pay) :
        
        if int(pay) != int(self.controller.cache["price"]) :
            self.raise_info_label_text_set("IMPROPER PAYMENT!!", "danger")
            return False
        
        else : return True 
        
            
    def send_payload_payment(self) :
        if self.radio_var.get() == "credit" :
            if self.validate_balance(self.balance_credit_input.get()) :           
                payment_payload = {"go_to":"paying", "body": {"method":"credit_card","card_id":self.credit_pass_input.get() ,"cvc":self.cvc_input.get(),"coupon_id":self.controller.cache["used_coupon"]}}
                self.controller.set_page_state(payment_payload)
        elif self.radio_var.get() == "promptpay" :
            if self.validate_balance(self.balance_promptpay_input.get()) :
                payment_payload = {"go_to":"paying", "body": {"method":"promptpay","tel":self.promptpay_input.get(),"coupon_id":self.controller.cache["used_coupon"]}}
                self.controller.set_page_state(payment_payload)

class Meal_Page(ttk.Frame) :
    def __init__(self, frame_controller) :
        super().__init__(frame_controller)
        
        self.pack(expand=True, fill=tk.BOTH)

        self.choose_meal_list = []
        self.controller = frame_controller
        self.create_widgets_meal()
        if self.controller.cache["user"] != None:
            self.create_user_info_frame()
        
    
    def calculate_total_price(self):
        self.total_price = sum([int(item["meal"].get()) * item["price"] for item in self.all_spinbox])
        new_meal_list = []
        for item in self.all_spinbox:
            if  int(item["meal"].get()) > 0 :
                new_meal_list.append({"meal_id": item["meal_id"],"amount":item["meal"].get()})
        self.choose_meal_list = new_meal_list
        self.set_sum_price()

    def set_sum_price(self) :
        self.total_label.config(text=f"Total Price from meals: {self.total_price}")

    def create_paylod(self):
        meal_payload = {"go_to":"summation_add_meal","body":{"price":int(self.total_price) +  int(self.controller.cache['price']),"meal_form":self.choose_meal_list}}
        return meal_payload
    def create_widgets_meal(self) :
        for widget in self.winfo_children(): widget.destroy()
        self.total_price = 0
        self.all_spinbox = []
        
        custom_font = ("Helvetica", 30)
        info = ("Helvetica", 13)
        
        header_frame = ttk.Frame(self, width=1200, height=200)
        header_frame.pack(pady=50)
        
        header_label = ttk.Label(header_frame, bootstyle="primary", text="Choose Meal", font=custom_font)
        header_label.pack()


        total_frame = ttk.LabelFrame(self,bootstyle='info')
        total_frame.pack()

        self.total_label = ttk.Label(total_frame, text=f'Total Price from meals: {self.total_price}')
        self.total_label.pack()

        list_frame = ScrolledFrame(self, width=1200, height=1000)
        list_frame.pack(side=TOP)

        self.image1 = PhotoImage(file='food01.png')
        self.resize_image1 = self.image1.subsample(7)

        self.image2 = PhotoImage(file='food02.png')
        self.resize_image2 = self.image2.subsample(7)

        self.image3 = PhotoImage(file='food03.png')
        self.resize_image3 = self.image3.subsample(7)

        self.image4 = PhotoImage(file='food04.png')
        self.resize_image4 = self.image4.subsample(7)

        self.image5 = PhotoImage(file='food05.png')
        self.resize_image5 = self.image5.subsample(7)

        meal_list = self.controller.cache['meals']
        count = 0
        for meal in meal_list:
                for menu,price in meal.items():
                    
                    image = [self.resize_image1,self.resize_image2,self.resize_image3,self.resize_image4,self.resize_image5]

                    Meal_frame = ttk.LabelFrame(list_frame, bootstyle='info')
                    Meal_frame.pack()

                    meal_name = ttk.Label(Meal_frame,image=image[count])
                    meal_name.pack(padx=10,side=LEFT, anchor=W,pady = 10 )

                    meal_price = ttk.Label(Meal_frame,text=f'Price:{price} ')
                    meal_price.pack(padx=10,pady=20,side=LEFT,anchor=W)

                    meal_count = ttk.Spinbox(Meal_frame, from_=0, to=10, command=self.calculate_total_price)
                    meal_count.set(0)
                    meal_count.pack(side=RIGHT,anchor=E)
                    
                    self.all_spinbox.append({"meal": meal_count, "price": price, "meal_id": menu})

                    count+=1
                    
        payload_back_button = {"go_to": "summation_from_meal"}
        back_button = ttk.Button(self, bootstyle="info", text="go back", command=lambda: self.controller.set_page_state(payload_back_button))
        back_button.place(x=10, y=500)

        submit_button = ttk.Button(list_frame,text='Submit',command=lambda: self.controller.set_page_state(self.create_paylod()))
        submit_button.pack()

    def create_user_info_frame(self) :
        user_frame = ttk.LabelFrame(self, text="USER INFO", bootstyle="info", width=350, height=120) 
        user_frame.place(relx=0.7, rely=0.78)


        name_label = ttk.Label(user_frame, bootstyle="inverse-info", text="Name :")
        name_label.grid(row=0, column=0, padx=5, pady=5)
        
        username_label = ttk.Label(user_frame, bootstyle="dark", text=f"{self.controller.cache["user"]["name"]}", width=20)
        username_label.grid(row=0, column=2, columnspan=2, padx=5, pady=5)
        
        payload_ticket_button = {"go_to":"ticket"}
        to_ticket_list_button = ttk.Button(user_frame, bootstyle="primary", text="see ticket", command=lambda: self.controller.set_page_state(payload_ticket_button))
        to_ticket_list_button.grid(row=1, column=0, padx=5, pady=5)
        
        payload_logout_button = {"go_to":"main_from_logout"}
        logout_button = ttk.Button(user_frame, bootstyle="primary", text="logout", command=lambda: self.controller.set_page_state(payload_logout_button))
        logout_button.grid(row=1, column=2, padx=5, pady=5)
                    
class Summation_Page(ttk.Frame) :
    def __init__(self, frame_controller) :
        super().__init__(frame_controller)
        
        self.pack(expand=True, fill=tk.BOTH)

        self.controller = frame_controller
        self.create_widgets_summation()   
        
        
        
    def create_widgets_summation(self) :
        self.coupon_id_input = tk.StringVar(value="")
        
        for widget in self.winfo_children(): widget.destroy()
        
        custom_font = ("Helvetica", 30)
        info = ("Helvetica", 13)
        
        header_frame = ttk.Frame(self, width=1200, height=200)
        header_frame.pack(pady=50)
        
        header_label = ttk.Label(header_frame, bootstyle="primary",text="Summation",font=custom_font)
        header_label.pack()
        
        data_frame = ttk.Frame(self)
        data_frame.pack()
        
        first_frame = ttk.LabelFrame(data_frame, bootstyle="primary", text=f"Reservation ID: {self.controller.cache["reservation_id"]}")
        first_frame.grid(row=0, column=0)
        
        span_label = ttk.Label(first_frame)
        span_label.pack(padx=100)
        
        train_label = ttk.Label(first_frame, text=f"Train ID: {self.controller.cache["train_id"]}", font=info)
        train_label.pack(anchor=tk.W, padx=8, pady=8)
        
        bogie_label = ttk.Label(first_frame, text=f"Bogie ID: {self.controller.cache["bogie_id"]}", font=info)
        bogie_label.pack(anchor=tk.W, padx=8, pady=8)
        
        seat_label = ttk.Label(first_frame, text=f"Seat List: {", ".join(self.controller.cache["reserved_seats"])}", font=info)
        seat_label.pack(anchor=tk.W, padx=8, pady=8)
        
        departure_station_label = ttk.Label(first_frame, text=f"Departure Station: {self.controller.cache["departure_station"].get()}", font=info)
        departure_station_label.pack(anchor=tk.W, padx=8, pady=8)
        
        destination_station_label = ttk.Label(first_frame, text=f"Destination Station: {self.controller.cache["destination_station"].get()}", font=info)
        destination_station_label.pack(anchor=tk.W, padx=8, pady=8)
        
        departure_time_label = ttk.Label(first_frame, text=f"Departure time: {self.controller.cache["departure_time"]}", font=info)
        departure_time_label.pack(anchor=tk.W, padx=8, pady=8)

        destination_time_label = ttk.Label(first_frame, text=f"Destination time: {self.controller.cache["destination_time"]}", font=info)
        destination_time_label.pack(anchor=tk.W, padx=8, pady=8)
        
        departure_time_label = ttk.Label(first_frame, text=f"Departure date: {self.controller.cache["departure_date"].entry.get()}", font=info)
        departure_time_label.pack(anchor=tk.W, padx=8, pady=8)
        
        second_frame = ttk.Frame(data_frame)
        second_frame.grid(row=0, column=1, padx=15)
        
        price_frame = ttk.LabelFrame(second_frame, bootstyle="primary", text="PRICE")
        price_frame.pack()
        
        
        self.price_label = ttk.Label(price_frame, bootstyle="success", text=f"{self.controller.cache["price"]} baht", font=info)
        self.price_label.pack(padx=20, pady=7)
        
        coupon_label = ttk.Label(price_frame, bootstyle="primary", text="Apply Coupon:", font=info)
        coupon_label.pack()
        
        coupon_entry = ttk.Entry(price_frame, bootstyle="primary",textvariable=self.coupon_id_input)
        coupon_entry.pack(padx=20, pady=7)
        
        error_label = ttk.Label(price_frame, bootstyle="primary", text="", font=info)
        error_label.pack()

        apply_coupon_button = ttk.Button(price_frame, bootstyle="primary", text="Apply", width=15, command=lambda:self.update_price(error_label,coupon_entry,apply_coupon_button))
        apply_coupon_button.pack(pady=7)
        
        payload_select_food_button = {"go_to": "meal"}
        select_food_button = ttk.Button(second_frame, bootstyle="success", text="Choose Meal", width=15, command=lambda: self.controller.set_page_state(payload_select_food_button))
        select_food_button.pack(pady=10)
        
        
        payload_payment_button = {"go_to": "pay"}
        payment_button = ttk.Button(second_frame, bootstyle="success", text="Pay", width=15, command=lambda: self.controller.set_page_state(payload_payment_button))
        payment_button.pack(pady=5)
        
    def update_price(self,error_label,coupon_entry,apply_coupon_button) :
        if self.validate_coupon() :
            error_label.config(text="Applied", foreground="green")
            coupon_entry.destroy()
            apply_coupon_button.destroy()
            self.controller.cache["price"] -= self.map_coupon_discount()
            self.controller.cache["used_coupon"] = self.coupon_id_input.get()
            self.update_price_label()
        else:
            error_label.config(text="Invalid", foreground="red")
            
    def update_price_label(self) :
        if int(self.controller.cache["price"]) < 0:
            self.price_label.config(text=f"0 baht")
        else:
            self.price_label.config(text=f"{self.controller.cache["price"]} baht")

    def validate_coupon(self) :
        for coupon in self.controller.cache["coupon_list"] :
            print(coupon["coupon_id"])
            print(self.coupon_id_input.get())
            if coupon["coupon_id"] == self.coupon_id_input.get() :
                return True
        return False
    
    def map_coupon_discount(self) :
        
        for coupon in self.controller.cache["coupon_list"] :
            if coupon["coupon_id"] == self.coupon_id_input.get() :
                return coupon["discount"]
        return 0
    
    def create_user_info_frame(self) :
        user_frame = ttk.LabelFrame(self, text="USER INFO", bootstyle="info", width=350, height=120) 
        user_frame.place(relx=0.7, rely=0.78)


        name_label = ttk.Label(user_frame, bootstyle="inverse-info", text="Name :")
        name_label.grid(row=0, column=0, padx=5, pady=5)
        
        username_label = ttk.Label(user_frame, bootstyle="dark", text=f"{self.controller.cache["user"]["name"]}", width=20)
        username_label.grid(row=0, column=2, columnspan=2, padx=5, pady=5)
        
        payload_ticket_button = {"go_to":"ticket"}
        to_ticket_list_button = ttk.Button(user_frame, bootstyle="primary", text="see ticket", command=lambda: self.controller.set_page_state(payload_ticket_button))
        to_ticket_list_button.grid(row=1, column=0, padx=5, pady=5)
        
        payload_logout_button = {"go_to":"main_from_logout"}
        logout_button = ttk.Button(user_frame, bootstyle="primary", text="logout", command=lambda: self.controller.set_page_state(payload_logout_button))
        logout_button.grid(row=1, column=2, padx=5, pady=5)

class Seat_page(ttk.Frame) :
    def __init__(self, frame_controller) :
        super().__init__(frame_controller)
        
        self.pack(expand=True, fill=tk.BOTH)

        self.controller = frame_controller
        self.create_widgets_seat()
        if self.controller.cache["user"] != None:
            self.create_user_info_frame()
        self.seat_payload_list = []
        self.count = 0
        
    def create_payload(self, seat) :
        if seat not in self.seat_payload_list :
            self.seat_payload_list.append(seat)
        elif seat in self.seat_payload_list :
            self.seat_payload_list.remove(seat)
        print(self.seat_payload_list)
        
    def validate_input(self, warning_label) :
        if len(self.seat_payload_list) < int(self.controller.cache["amount"].get()) :
            number = int(self.controller.cache["amount"].get()) - len(self.seat_payload_list)
            warning_label.config(text=f"you have to choose more {number} place")
            return False
        elif len(self.seat_payload_list) > int(self.controller.cache["amount"].get()) :
            number = len(self.seat_payload_list) - int(self.controller.cache["amount"].get())
            warning_label.config(text=f"you have to unpick {number} place")
            return False
        else : return True
        
    def send_payload(self, req_label) :
        if self.validate_input(req_label) :
            payload_choose_seat = {"go_to": "summation", "body": {"seats": self.seat_payload_list, "error": req_label}}
            self.controller.set_page_state(payload_choose_seat)
         
        
    def create_widgets_seat(self) :
        for widget in self.winfo_children(): widget.destroy()
        self.count = 0
        
        seat_list = self.controller.cache["available_seat_list"]
        
        custom_font = ("Helvetica", 30)
        req = ("Helvetica", 15)
        
        header_frame = ttk.Frame(self, width=1200, height=200)
        header_frame.pack(pady=50)
        
        header_label = ttk.Label(header_frame,bootstyle="primary",text="CHOOSE SEAT",font=custom_font)
        header_label.pack()
        
        req_label = ttk.Label(header_frame,bootstyle="info",text=f"please choose {self.controller.cache["amount"].get()} seats",font=req)
        req_label.pack(pady=10)
        
        seat_frame = ttk.Frame(self)
        seat_frame.pack()
        
        self.img1 = PhotoImage(file='armchair.png')
        self.resize_image = self.img1.subsample(7)
        
        position_row = 0
        position_col = 0
        for data in seat_list :

            if position_row == 2 :
                position_row = 0
                position_col += 1 

            sub_seat_frame = ttk.Frame(seat_frame)
            sub_seat_frame.grid(row=position_row, column=position_col)

            seat_button = ttk.Checkbutton(sub_seat_frame,image=self.resize_image, bootstyle="info-outline-toolbutton", text=f"seat no: {data["seat_no"]}", width=15, command=lambda seat = data["seat_no"] : self.create_payload(seat))
            seat_button.pack(padx=20, pady=10)

            text = ttk.Label(sub_seat_frame, text=f"     seat no: {data["seat_no"]}", width=15)
            text.pack(padx=15, pady=5)

            position_row += 1
        
        warning_label = ttk.Label(self, bootstyle="danger", text="")
        warning_label.pack(pady=(20,0)) 

        confirm_buttun = ttk.Button(self, bootstyle="seccess", text="Confirm", command=lambda : self.send_payload(warning_label))
        confirm_buttun.pack(pady=10)

        payload_back_button = {"go_to": "bogie","body": {"train_id":self.controller.cache["train_id"], "departure_time": self.controller.cache["departure_time"], "destination_time": self.controller.cache["destination_time"]}}
        back_button = ttk.Button(self, bootstyle="info", text="go back", command=lambda: self.controller.set_page_state(payload_back_button))
        back_button.pack(side=tk.BOTTOM, anchor=tk.W, padx=10, pady=(0,10))


    def create_user_info_frame(self) :
        user_frame = ttk.LabelFrame(self, text="USER INFO", bootstyle="info", width=350, height=120) 
        user_frame.place(relx=0.7, rely=0.78)


        name_label = ttk.Label(user_frame, bootstyle="inverse-info", text="Name :")
        name_label.grid(row=0, column=0, padx=5, pady=5)
        
        username_label = ttk.Label(user_frame, bootstyle="dark", text=f"{self.controller.cache["user"]["name"]}", width=20)
        username_label.grid(row=0, column=2, columnspan=2, padx=5, pady=5)
        
        payload_ticket_button = {"go_to":"ticket"}
        to_ticket_list_button = ttk.Button(user_frame, bootstyle="primary", text="see ticket", command=lambda: self.controller.set_page_state(payload_ticket_button))
        to_ticket_list_button.grid(row=1, column=0, padx=5, pady=5)
        
        payload_logout_button = {"go_to":"main_from_logout"}
        logout_button = ttk.Button(user_frame, bootstyle="primary", text="logout", command=lambda: self.controller.set_page_state(payload_logout_button))
        logout_button.grid(row=1, column=2, padx=5, pady=5)

        

class Bogie_Page(ttk.Frame) :
    def __init__(self, frame_controller) :
        super().__init__(frame_controller)
        
        self.pack(expand=True, fill=tk.BOTH)

        self.controller = frame_controller
        self.create_widgets_bogie()
        
        if self.controller.cache["user"] != None:
            self.create_user_info_frame()
        
    def create_widgets_bogie(self) :
        
        custom_font = ("Helvetica", 30)
        info_font = ("Helvetica", 14)
        
        bogie_list = self.controller.result_bogie_list
        

        header_frame = ttk.Frame(self, width=1200, height=100)
        header_frame.pack(pady=40, side=tk.TOP)

        header_label = ttk.Label(header_frame,bootstyle="info",text="Choose Bogie",font=custom_font)
        header_label.pack()
        
        picture_frame = ttk.Frame(self)
        picture_frame.pack()



        # Keep a reference to the PhotoImage object
        self.photo = tk.PhotoImage(file='vehicle.png')
        self.resized_image = self.photo.subsample(4)
        image_label = ttk.Label(
            picture_frame,
            image=self.resized_image,
            padding=5
        )
        image_label.grid(padx = 100)
        image_label.lift()
        
        list_frame = ttk.Frame(self, width=1200, height=100)
        list_frame.pack(side=tk.TOP)
        
        for data in bogie_list :
            key = next(iter(data.keys()))
            sub_key_list = [sub_key for sub_key in data[key]]

            
            train_frame = ttk.LabelFrame(list_frame, bootstyle="info", text=f"bogie id: {key}", width=800, height=50)
            train_frame.pack(padx=10, pady=10)
            
            info_train = ttk.Label(train_frame, text=f" In     {data[key][sub_key_list[0]]}    ", font=info_font)
            info_train.grid(row=0, column=0, pady=10)
            
            if self.controller.cache["user"] != None: payload_choose_bogie_button = {"go_to": "seat", "body": {"train_id": data[key][sub_key_list[0]], "bogie_id": key}}
            else : payload_choose_bogie_button = {"go_to": "login_from_bogie"}
            choose_choose_button = ttk.Button(train_frame, text="choose", bootstyle="info", command=lambda payload=payload_choose_bogie_button: self.controller.set_page_state(payload))
            choose_choose_button.grid(row=0, column=5, sticky=tk.E, padx=10)
        
        payload_back_button = {"go_to": "train","body": {"combo_departure":self.controller.cache["departure_station"], "combo_destination": self.controller.cache["destination_station"], "my_date": self.controller.cache["departure_date"], "entry_amount": self.controller.cache["amount"]}}
        back_button = ttk.Button(self, bootstyle="info", text="go back", command=lambda: self.controller.set_page_state(payload_back_button))
        back_button.pack(side=tk.BOTTOM, anchor=tk.W, padx=10, pady=40)
    
    def create_user_info_frame(self) :
        user_frame = ttk.LabelFrame(self, text="USER INFO", bootstyle="info", width=350, height=120) 
        user_frame.place(relx=0.7, rely=0.78)

        name_label = ttk.Label(user_frame, bootstyle="inverse-info", text="Name :")
        name_label.grid(row=0, column=0, padx=5, pady=5)
        
        username_label = ttk.Label(user_frame, bootstyle="dark", text=f"{self.controller.cache["user"]["name"]}", width=20)
        username_label.grid(row=0, column=2, columnspan=2, padx=5, pady=5)
        
        payload_ticket_button = {"go_to":"ticket"}
        to_ticket_list_button = ttk.Button(user_frame, bootstyle="primary", text="see ticket", command=lambda: self.controller.set_page_state(payload_ticket_button))
        to_ticket_list_button.grid(row=1, column=0, padx=5, pady=5)
        
        payload_logout_button = {"go_to":"main_from_logout"}
        logout_button = ttk.Button(user_frame, bootstyle="primary", text="logout", command=lambda: self.controller.set_page_state(payload_logout_button))
        logout_button.grid(row=1, column=2, padx=5, pady=5)

        
class Train_Page(ttk.Frame) :
    def __init__(self, frame_controller) :
        super().__init__(frame_controller)
        
        self.pack(expand=True, fill=tk.BOTH)

        self.controller = frame_controller
        self.create_widgets_train()
        
        if self.controller.cache["user"] != None:
            self.create_user_info_frame()
        
    def create_widgets_train(self) :
        route_list = self.controller.result_route_list
        # print(route_list)
        
        custom_font = ("Helvetica", 30)
        info_font = ("Helvetica", 14)

        header_frame = ttk.Frame(self, width=1200, height=100)
        header_frame.pack(pady=40, side=tk.TOP)

        header_label = ttk.Label(header_frame,bootstyle="info",text="Choose Train",font=custom_font)
        header_label.pack()
        
        picture_frame = ttk.Frame(self)
        picture_frame.pack()

        # Keep a reference to the PhotoImage object
        self.photo = tk.PhotoImage(file='train2.png')
        self.resized_image = self.photo.subsample(5)
        image_label = ttk.Label(
            picture_frame,
            image=self.resized_image,
            padding=5
        )
        image_label.grid()
        image_label.lift()
        
        list_frame = ttk.Frame(self, width=1200, height=100)
        list_frame.pack(side=tk.TOP)
        
        # print(route_list)
        
        for data in route_list :
            key = next(iter(data.keys()))
            sub_key_list = [sub_key for sub_key in data[key]]
            
            train_frame = ttk.LabelFrame(list_frame, bootstyle="info", text=f"train id: {key}", width=800, height=50)
            train_frame.pack(padx=10, pady=10)
            
            info_departure_station = ttk.Label(train_frame, text=f"{data[key][sub_key_list[0]]}----->", font=info_font)
            info_departure_station.grid(row=0, column=0, pady=10)
            
            info_destination_station = ttk.Label(train_frame, text=f"{data[key][sub_key_list[1]]}", font=info_font)
            info_destination_station.grid(row=0, column=1, sticky=tk.W)
            
            info_departure_time_station = ttk.Label(train_frame, text=f"    departure time: {data[key][sub_key_list[2]]} ----->", font=info_font)
            info_departure_time_station.grid(row=1, column=0)
            
            info_destination_time_station = ttk.Label(train_frame, text=f"destination time: {data[key][sub_key_list[3]]}   ", font=info_font)
            info_destination_time_station.grid(row=1, column=1)
            
            info_destination_date_station = ttk.Label(train_frame, text=f"@   destination date: {data[key][sub_key_list[4]]}", font=info_font)
            info_destination_date_station.grid(row=1, column=2)

            payload_choose_train_button = {"go_to": "bogie", "body": {"train_id": key, "departure_time": data[key][sub_key_list[2]], "destination_time": data[key][sub_key_list[3]]}}
            choose_train_button = ttk.Button(train_frame, text="choose", bootstyle="info", command=lambda payload=payload_choose_train_button: self.controller.set_page_state(payload))
            choose_train_button.grid(row=0, column=5, sticky=tk.E, padx=10)

        payload_back_button = {"go_to": "route"}
        back_button = ttk.Button(self, bootstyle="info", text="go back", command=lambda: self.controller.set_page_state(payload_back_button))
        back_button.pack(side=tk.BOTTOM, anchor=tk.W, padx=10, pady=40)
        
    def create_user_info_frame(self) :
        user_frame = ttk.LabelFrame(self, text="USER INFO", bootstyle="info", width=350, height=120) 
        user_frame.place(relx=0.7, rely=0.78)

        name_label = ttk.Label(user_frame, bootstyle="inverse-info", text="Name :")
        name_label.grid(row=0, column=0, padx=5, pady=5)
        
        username_label = ttk.Label(user_frame, bootstyle="dark", text=f"{self.controller.cache["user"]["name"]}", width=20)
        username_label.grid(row=0, column=2, columnspan=2, padx=5, pady=5)
        
        payload_ticket_button = {"go_to":"ticket"}
        to_ticket_list_button = ttk.Button(user_frame, bootstyle="primary", text="see ticket", command=lambda: self.controller.set_page_state(payload_ticket_button))
        to_ticket_list_button.grid(row=1, column=0, padx=5, pady=5)
        
        payload_logout_button = {"go_to":"main_from_logout"}
        logout_button = ttk.Button(user_frame, bootstyle="primary", text="logout", command=lambda: self.controller.set_page_state(payload_logout_button))
        logout_button.grid(row=1, column=2, padx=5, pady=5)

class Route_Page(ttk.Frame) :
    def __init__(self, frame_controller) :
        super().__init__(frame_controller)
        
        self.pack(expand=True, fill=tk.BOTH)

        self.controller = frame_controller
        self.create_widgets_route()   
        
        if self.controller.cache["user"] != None:
            self.create_user_info_frame()
        
    def create_widgets_route(self):
        
        element_theme = "success"
        stations_list = self.controller.all_station_list
        # print(stations_list)
        
        custom_font = ("Helvetica", 30)

        header_frame = ttk.Frame(self, width=1200, height=100)
        header_frame.pack(pady=40)

        header_label = ttk.Label(header_frame,bootstyle="info",text="Train Ticket Reservation",font=custom_font,)
        header_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        picture_frame = ttk.Frame(self)
        picture_frame.pack()

        # Keep a reference to the PhotoImage object
        self.photo = tk.PhotoImage(file='destination.png')
        self.resized_image = self.photo.subsample(5)
        image_label = ttk.Label(
            picture_frame,
            image=self.resized_image,
            padding=5
        )
        image_label.grid()
        image_label.lift()

        form_frame = ttk.Labelframe(self, text="select route", bootstyle="primary", width=1000, height=400)
        form_frame.pack(pady=50)

        label_departure = ttk.Label(form_frame, bootstyle=element_theme, text="Departure:")
        label_departure.grid(row=0, column=0, padx=10, pady=5)
        combo_departure = ttk.Combobox(form_frame,bootstyle=element_theme,values=[station["station name"] for station in stations_list],)
        combo_departure.grid(row=0, column=1, padx=10, pady=5)

        label_destination = ttk.Label(form_frame, bootstyle=element_theme, text="Destination:")
        label_destination.grid(row=0, column=2, padx=10, pady=5)
        combo_destination = ttk.Combobox(form_frame,bootstyle=element_theme,values=[station["station name"] for station in stations_list],)
        combo_destination.grid(row=0, column=3, padx=10, pady=5)

        label_date = ttk.Label(form_frame, bootstyle=element_theme, text="Choose Date:")
        label_date.grid(row=0, column=4, padx=10, pady=5)
        my_date = ttk.DateEntry(form_frame, bootstyle=element_theme, width=12,dateformat='%Y-%m-%d')
        my_date.grid(row=0, column=5, padx=10, pady=5)

        label_amount = ttk.Label(form_frame, bootstyle=element_theme, text="Amount:")
        label_amount.grid(row=0, column=6, padx=10, pady=5)
        
        entry_amount = ttk.Spinbox(form_frame,from_= 1, to=5, bootstyle=element_theme)
        entry_amount.grid(row=0, column=7, padx=10, pady=5)

        error_label = ttk.Label(form_frame, text="", foreground="red")
        error_label.grid(row=1, column=3)

        payload_submit_button = {"go_to": "train", "body": {"combo_departure":combo_departure, "combo_destination": combo_destination, "my_date": my_date, "entry_amount": entry_amount,"error":error_label}}
        submit_button = ttk.Button(form_frame,bootstyle=element_theme,text="Submit",command=lambda: self.controller.set_page_state(payload_submit_button))
        submit_button.grid(row=0, column=8, padx=5, pady=10)

        payload_back_button = {"go_to": "main"}
        back_button = ttk.Button(self, bootstyle="info", text="go back", command=lambda: self.controller.set_page_state(payload_back_button))
        back_button.pack(side=tk.BOTTOM, anchor=tk.W, padx=10, pady=40)
    
    def create_user_info_frame(self) :
        user_frame = ttk.LabelFrame(self, text="USER INFO", bootstyle="info", width=350, height=120) 
        user_frame.place(relx=0.7, rely=0.78)

        name_label = ttk.Label(user_frame, bootstyle="inverse-info", text="Name :")
        name_label.grid(row=0, column=0, padx=5, pady=5)
        
        username_label = ttk.Label(user_frame, bootstyle="dark", text=f"{self.controller.cache["user"]["name"]}", width=20)
        username_label.grid(row=0, column=2, columnspan=2, padx=5, pady=5)
        
        payload_ticket_button = {"go_to":"ticket"}
        to_ticket_list_button = ttk.Button(user_frame, bootstyle="primary", text="see ticket", command=lambda: self.controller.set_page_state(payload_ticket_button))
        to_ticket_list_button.grid(row=1, column=0, padx=5, pady=5)
        
        payload_logout_button = {"go_to":"main_from_logout"}
        logout_button = ttk.Button(user_frame, bootstyle="primary", text="logout", command=lambda: self.controller.set_page_state(payload_logout_button))
        logout_button.grid(row=1, column=2, padx=5, pady=5)

        
class Register_Page(ttk.Frame) :
    def __init__(self, frame_controller) :
        super().__init__(frame_controller)
        
        self.pack(expand=True, fill=tk.BOTH)

        self.controller = frame_controller
        self.create_widgets_register()

    def create_widgets_register(self) :
        custom_font = ("Helvetica", 30)

        header_frame = ttk.Frame(self, width=1200, height=200)
        header_frame.pack(side=tk.TOP)
        
        header_label = ttk.Label(header_frame, bootstyle="info", text="REGISTER", font=custom_font)
        header_label.pack(pady=50)
        
        main_menu_frame = ttk.Frame(self)
        main_menu_frame.pack(side=tk.TOP)
        
        form_label = ttk.Label(main_menu_frame, bootstyle="inverse-light", font=custom_font)
        form_label.pack(side=tk.TOP, expand=True, fill=tk.Y)
        
        # configure the grid
        form_label.columnconfigure(0, weight=1)
        form_label.columnconfigure(1, weight=3)

        # name
        name_label = ttk.Label(form_label, text="Name:")
        name_label.grid(column=0, row=0, sticky=tk.W, padx=20, pady=20)

        name_entry = ttk.Entry(form_label)
        name_entry.grid(column=1, row=0, sticky=tk.E, padx=20, pady=20)
        
        # username
        username_label = ttk.Label(form_label, text="Username:")
        username_label.grid(column=0, row=1, sticky=tk.W, padx=20, pady=20)

        username_entry = ttk.Entry(form_label)
        username_entry.grid(column=1, row=1, sticky=tk.E, padx=20, pady=20)

        # password
        password_label = ttk.Label(form_label, text="Password:")
        password_label.grid(column=0, row=2, sticky=tk.W, padx=20, pady=20)

        password_entry = ttk.Entry(form_label,  show="*")
        password_entry.grid(column=1, row=2, sticky=tk.E, padx=20, pady=20)
        
        #! Edited: change name
        # password
        confirm_label = ttk.Label(form_label, text="Confirm Password:")
        confirm_label.grid(column=0, row=3, sticky=tk.W, padx=20, pady=20)
        
        
        # confirm password
        confirm_entry = ttk.Entry(form_label,  show="*")
        confirm_entry.grid(column=1, row=3, sticky=tk.E, padx=20, pady=20)

        
        error_label = ttk.Label(form_label, text="", foreground="red",bootstyle="inverse-light")
        error_label.grid(row=4, columnspan=2)

       
        # register button
        payload_register_button = {"username":username_entry, "name":name_entry, "password":password_entry, "confirm":confirm_entry, "error":error_label}
        register_button = ttk.Button(form_label, text="Register", command=lambda : self.controller.submit_register(payload_register_button))
        register_button.grid(column=1, row=4, sticky=tk.E, padx=20, pady=20)
        
        if self.controller.cache["register from login"]:
            payload_back_button = {"go_to": "login_from_register"}
        else:
            payload_back_button = {"go_to":"main"}
        back_button = ttk.Button(self, bootstyle="info", text="go back", command=lambda: self.controller.set_page_state(payload_back_button))
        back_button.pack(side=tk.BOTTOM, anchor=tk.W, padx=10, pady=40)

    def create_user_info_frame(self) :
        pass
    
class Login_Page(ttk.Frame) :
    def __init__(self, frame_controller) :
        super().__init__(frame_controller)
        
        self.pack(expand=True, fill=tk.BOTH)

        self.controller = frame_controller
        self.create_widgets_login()

    def create_widgets_login(self) :
        custom_font = ("Helvetica", 30)

        header_frame = ttk.Frame(self, width=1200, height=200)
        header_frame.pack(side=tk.TOP)

        picture_frame = ttk.Frame(self)
        picture_frame.pack()

        #image
        self.photo_info = tk.PhotoImage(file='file.png')
        self.resized_image = self.photo_info.subsample(6)
        image_label = ttk.Label(
             picture_frame,
            image=self.resized_image,
            padding=5
        )
        image_label.grid(row=0, column=0, sticky=tk.W, padx=100, pady=40)
        
        header_label = ttk.Label(header_frame,bootstyle="info",text="LOGIN",font=custom_font)
        header_label.pack(pady=(40, 10))
        
        main_menu_frame = ttk.Frame(self)
        main_menu_frame.pack(side=tk.TOP)

        # form label
        form_label = ttk.Label(main_menu_frame, bootstyle="inverse-light", font=custom_font)
        form_label.grid(row=1, column=0, sticky=tk.NSEW)
        
        # configure the grid
        form_label.columnconfigure(0, weight=1)
        form_label.columnconfigure(1, weight=3)

        # username
        username_label = ttk.Label(form_label, text="Username:")
        username_label.grid(column=0, row=0, sticky=tk.W, padx=20, pady=20)

        username_entry = ttk.Entry(form_label)
        username_entry.grid(column=1, row=0, sticky=tk.E, padx=20, pady=20)

        # password
        password_label = ttk.Label(form_label, text="Password:")
        password_label.grid(column=0, row=1, sticky=tk.W, padx=20, pady=20)

        password_entry = ttk.Entry(form_label,  show="*")
        password_entry.grid(column=1, row=1, sticky=tk.E, padx=20, pady=20)
        
        if self.controller.cache["login from bogie"]:
            error_label = ttk.Label(form_label, text="please login to proceed", foreground="red",bootstyle="inverse-light")
            payload_login_button = {"go_to": "bogie_from_login", "body": {"username" : username_entry, "password" : password_entry,"error":error_label}}
            payload_back_button = {"go_to": "bogie","body": {"train_id": self.controller.cache["train_id"], "departure_time": self.controller.cache["departure_time"], "destination_time": self.controller.cache["departure_time"]}}
        else:
            error_label = ttk.Label(form_label, text="", foreground="red",bootstyle="inverse-light")
            payload_login_button = {"go_to": "main_from_login_reg", "body": {"username" : username_entry, "password" : password_entry,"error":error_label}}
            payload_back_button = {"go_to": "main"}
        error_label.grid(row=2, columnspan=2)
        
        # login button
        
        login_button = ttk.Button(form_label, text="Login", command= lambda: self.controller.set_page_state(payload_login_button))
        login_button.grid(column=1, row=3, sticky=tk.E, padx=20, pady=10)
        
        payload_register_button = {"go_to": "register_from_login"}
        to_register_button = ttk.Button(self, bootstyle="primary-outline", text="REGISTER", width=20, command=lambda: self.controller.set_page_state(payload_register_button))
        to_register_button.pack(pady=12)
        back_button = ttk.Button(self, bootstyle="info", text="go back", command=lambda: self.controller.set_page_state(payload_back_button))
        back_button.pack(side=tk.BOTTOM, anchor=tk.W, padx=10, pady=(0,20))
    
    def create_user_info_frame(self) :
        pass
    
class Ticket_Page(ttk.Frame):
    def __init__(self, frame_controller) :
        super().__init__(frame_controller)
        
        self.pack(expand=True, fill=tk.BOTH)

        self.controller = frame_controller
        
        self.create_widgets_ticket()
        
    def create_widgets_ticket(self) :
        for widget in self.winfo_children(): widget.destroy()
        custom_font = ("Helvetica", 30)
        info_font = ("Helvetica", 14)

        

        list_frame = ScrolledFrame(self, width=1200, height=1000)
        list_frame.pack(side=tk.TOP)
        
        header_frame = ttk.Frame(list_frame, width=1200, height=200)
        header_frame.pack(side=tk.TOP)

        header_label = ttk.Label(header_frame,bootstyle="info",text="Tickets",font=custom_font)
        header_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # print(route_list)
        ticket_list = self.controller.cache["ticket_list"]
        for data in ticket_list:
            ticket_frame = ttk.LabelFrame(list_frame, bootstyle="info", text=f"Ticket ID: {data["ticket_ID"]}", width=900, height=350)
            ticket_frame.pack(padx=10, pady=10)
            
            info_reservation_id = ttk.Label(ticket_frame, text=f"Reservation ID: {data["reservation_ID"]} ", font=info_font)
            info_reservation_id.grid(padx=10, row=0, column=0, pady=10, sticky=W)
            
            info_train_id = ttk.Label(ticket_frame, text=f"Train ID: {data["train_ID"]} ", font=info_font)
            info_train_id.grid(padx=10, row=1, column=0, sticky=W)
            
            info_bogie_id = ttk.Label(ticket_frame, text=f"Bogie ID: {data["bogie_ID"]} ", font=info_font)
            info_bogie_id.grid(padx=10, row=1, column=1, sticky=W)
            
            info_seat_id = ttk.Label(ticket_frame, text=f"Seat ID: {data["seat_ID"]} ", font=info_font)
            info_seat_id.grid(padx=10, row=1, column=2, sticky=W)
            
            info_departure_station = ttk.Label(ticket_frame, text=f"Departure Station: {data["departure Station"]} ", font=info_font)
            info_departure_station.grid(padx=10, row=2, column=0, sticky=W)

            info_destination_station = ttk.Label(ticket_frame, text=f"Destination Station: {data["destination Station"]} ", font=info_font)
            info_destination_station.grid(padx=10, row=2, column=1, sticky=W)
            
            info_departure_time = ttk.Label(ticket_frame, text=f"Departure: {data["departure Time"]} ", font=info_font)
            info_departure_time.grid(padx=10, row=3, column=0, sticky=W)

            info_destination_time = ttk.Label(ticket_frame, text=f"Destination: {data["destination Time"]} ", font=info_font)
            info_destination_time.grid(padx=10, row=3, column=1, sticky=W)

            info_destination_date = ttk.Label(ticket_frame, text=f"Date: {data["date"]} ", font=info_font)
            info_destination_date.grid(padx=10, row=3, column=2, sticky=W)

            error_label = ttk.Label(ticket_frame, text="", foreground="red",bootstyle="inverse-light")
            error_label.grid(padx=10, row=4, column=1, sticky=W)

            payload_cancel_button = {"ticket_id": data["ticket_ID"],"departure_time": data["departure Time"], "departure_date": data["date"], "error": error_label}
            choose_train_button = ttk.Button(ticket_frame, text="Cancel", bootstyle=DANGER, command=lambda payload=payload_cancel_button: self.controller.submit_cancel(payload))
            choose_train_button.grid(row=1, column=5, sticky=tk.E, padx=10)

        payload_back_button = {"go_to": "main"}
        back_button = ttk.Button(list_frame, bootstyle="info", text="go back", command=lambda: self.controller.set_page_state(payload_back_button))
        back_button.pack(side=tk.BOTTOM, anchor=tk.W, padx=10, pady=(0,10))
        
class Main_Page(ttk.Frame) :
    def __init__(self, frame_controller) :
        super().__init__(frame_controller)
        
        self.pack(expand=True, fill=tk.BOTH)

        self.controller = frame_controller
        self.create_widgets_main()
    
    def create_widgets_main(self) :
        for widget in self.winfo_children(): widget.destroy()
        
        custom_font = ("Helvetica", 30)
        
        header_frame = ttk.Frame(self, width=1200, height=200)
        header_frame.pack()
        
        header_label = ttk.Label(header_frame,bootstyle="info",text="TRAIN TICKET RESERVATION",font=custom_font)
        header_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        main_menu_frame = ttk.Frame(self)
        main_menu_frame.pack()
        
        # Keep a reference to the PhotoImage object
        self.photo = tk.PhotoImage(file='train.png')
        self.resized_image = self.photo.subsample(5)
        image_label = ttk.Label(
            main_menu_frame,
            image=self.resized_image,
            padding=5
        )
        image_label.pack()
        image_label.lift()
        
        payload_reservation_button = {"go_to": "route"}
        to_reservation_button = ttk.Button(main_menu_frame, bootstyle="success", text="RESERVATION", width=20, command=lambda: self.controller.set_page_state(payload_reservation_button))
        to_reservation_button.pack(pady=12)
        
        payload_login_button = {"go_to": "login"}
        self.to_login_button = ttk.Button(main_menu_frame, bootstyle="primary", text="LOGIN", width=20, command=lambda: self.controller.set_page_state(payload_login_button))
        self.to_login_button.pack(pady=12)
        
        payload_register_button = {"go_to": "register"}
        self.to_register_button = ttk.Button(main_menu_frame, bootstyle="primary-outline", text="REGISTER", width=20, command=lambda: self.controller.set_page_state(payload_register_button))
        self.to_register_button.pack(pady=12)
    
    def hide_login_and_register_button(self) :
        self.to_login_button.pack_forget()
        self.to_register_button.pack_forget()
    
    def show_login_and_register_button(self):
        self.to_login_button.pack(pady=12)
        self.to_register_button.pack(pady=12)
    
    def create_user_info_frame(self) :
        self.user_frame = ttk.LabelFrame(self, text="USER INFO", bootstyle="info", width=350, height=120) 
        self.user_frame.place(relx=0.7, rely=0.78)
        user_frame = self.user_frame

        name_label = ttk.Label(user_frame, bootstyle="inverse-info", text="Name :")
        name_label.grid(row=0, column=0, padx=5, pady=5)
        
        username_label = ttk.Label(user_frame, bootstyle="dark", text=f"{self.controller.cache["user"]["name"]}", width=20)
        username_label.grid(row=0, column=2, columnspan=2, padx=5, pady=5)
        
        payload_ticket_button = {"go_to":"ticket"}
        to_ticket_list_button = ttk.Button(user_frame, bootstyle="primary", text="see ticket", command=lambda: self.controller.set_page_state(payload_ticket_button))
        to_ticket_list_button.grid(row=1, column=0, padx=5, pady=5)
        
        payload_logout_button = {"go_to":"main_from_logout"}
        logout_button = ttk.Button(user_frame, bootstyle="primary", text="logout", command=lambda: self.controller.set_page_state(payload_logout_button))
        logout_button.grid(row=1, column=2, padx=5, pady=5)
        
class FrameController(ttk.Frame) :
    def __init__(self, root) :
        super().__init__(root)
        
        # self["bootstyle"] = SECONDARY
        self.pack(expand=True, fill=tk.BOTH)
        
        
        # self.selected_value = tk.StringVar()
        
        self.__frames = {}
        self.__frames["main"] = Main_Page(self)
        
        #change
        self.__cache = {
            "user" : None,
            "route_list" : None,
            "train_id" : None,
            "bogie_id" : None,
            "reservation_id" : None,
            "departure_station" : None,
            "destination_station" : None,
            "departure_time" : None,
            "destination_time" : None,
            "departure_date" : None,
            "amount" : None,
            "in_route_fetched": False,
            "available_seat_list" : [],
            "login from bogie": False,
            "register from login": False,
            "used_coupon": None
        }
        
        self.set_page_state({"go_to": "main"})
        
    @property
    def cache(self) :
        return self.__cache
    
    @property
    def all_station_list(self) :
        return self.__all_station_list
        
    @property
    def result_route_list(self) :
        return self.__result_route_list
    
    @property
    def result_bogie_list(self) :
        return self.__result_bogie_list
    
    @property
    def result_seat_list(self) :
        return self.__result_seat_list
    
    def set_page_state(self, payload):
        if payload["go_to"] == "login":
            self.__frames["login"] = Login_Page(self)

        elif payload["go_to"] == "login_from_bogie":
            self.cache["login from bogie"] = True
            self.__frames["login"] = Login_Page(self)
            payload["go_to"] = "login"

        elif payload["go_to"] == "login_from_register":
            self.cache["register from login"] = False
            self.__frames["login"].destroy()
            self.__frames["login"] = Login_Page(self)
            payload["go_to"] = "login"
        
        elif payload["go_to"] == "bogie_from_login":
            response = self.validate("login",payload["body"])
            if response != "pass":
                return
            response = self.submit_login(payload["body"])
            if response == "error" :
                return
            self.__frames["main"].create_user_info_frame()
            self.__frames["main"].hide_login_and_register_button()
            self.cache["login from bogie"] = False
            self.__frames["bogie"].destroy()
            self.__frames["bogie"] = Bogie_Page(self)
            payload["go_to"] = "bogie"

        elif payload["go_to"] == "register":
            self.__frames["register"] = Register_Page(self)

        elif payload["go_to"] == "register_from_login":
            self.cache["register from login"] = True
            self.__frames["register"] = Register_Page(self)
            payload["go_to"] = "register"
        elif payload["go_to"] == "ticket":

            self.__cache["ticket_list"] = FrameController.fetch_ticket_list(self.cache["user"]["member_id"])
            self.__frames["ticket"] = Ticket_Page(self)

        elif payload["go_to"] == "route" :
            self.__all_station_list = FrameController.request_all_route_list()
            self.__frames["route"] = Route_Page(self)
            
        elif payload["go_to"] == "train" :
            response = self.validate("train",payload["body"])
            if response != "pass":
                return
            response = self.submit_req_route(payload["body"])
            if response == "error":
                return
            self.__result_route_list = response
            self.__frames["train"] = Train_Page(self)
            
        elif payload["go_to"] == "bogie" :
            self.__result_bogie_list = self.submit_req_train(payload["body"])
            self.__frames["bogie"] = Bogie_Page(self)
        
        elif payload["go_to"] == "main_from_login_reg" :
            response = self.validate("login",payload["body"])
            if response != "pass":
                return
            response = self.submit_login(payload["body"])
            if response == "error" :
                return
            self.__frames["main"].create_user_info_frame()
            self.__frames["main"].hide_login_and_register_button()
            
            payload["go_to"] = "main"
        
        elif payload["go_to"] == "main_from_logout":
            self.submit_logout()
            self.__frames["main"].show_login_and_register_button()
            payload["go_to"] = "main"
            
        elif payload["go_to"] == "seat" :
            self.__result_seat_list = self.submit_req_bogie(payload["body"])
            self.__frames["seat"] = Seat_page(self)
        
        elif payload["go_to"] == "summation" :
            response = self.submit_req_seat(payload["body"])
            if response ==  "error" :
                return
            self.__frames["summation"] = Summation_Page(self)
        
        elif payload["go_to"] == "summation_from_pay" or payload["go_to"] == "summation_from_meal" :
            payload["go_to"] = "summation"
        
        elif payload["go_to"] == "summation_add_meal":
            response = self.submit_meal(payload["body"])
            self.__frames["summation"].update_price_label()
            payload["go_to"] = "summation"
        elif payload["go_to"] == "meal" :
            self.__frames["meal"] = Meal_Page(self)
            
        elif payload["go_to"] == "pay" :
            self.__frames["pay"] = Pay_Page(self)
            
        elif payload["go_to"] == "paying" :
            self.submit_payment(payload["body"])
            self.__frames["pay"].drop_aleart()
            self.__frames["pay"].drop_submit_button()
            self.__frames["pay"].raise_info_label_text_set("SUCCESS", "success")
            self.__frames["pay"].raise_main_menu_button()
            return
            

        for page in self.__frames.items() :
            page[1].pack_forget() if page[0] != payload["go_to"] else page[1].pack(expand=True, fill=tk.BOTH)
    def submit_payment(self,body):
        reservation_id = self.cache["reservation_id"]
        if body["method"] == "credit_card":
            payment_method = {body["method"]:[body["card_id"],body["cvc"]]}
        else:
            payment_method = {body["method"]:[body["tel"]]}
        coupon_id = body["coupon_id"]
        FrameController.fetch_payment(reservation_id,payment_method,coupon_id)

    def submit_meal(self,body):
        reservation_id = self.cache["reservation_id"]
        total_price_by_adding_food_from_UI = body["price"]
        meal_form = body["meal_form"]
        response = FrameController.fetch_meal(reservation_id,total_price_by_adding_food_from_UI,meal_form)
        self.cache["price"] = response["price"]
    def submit_req_seat(self, body) :
        #! สรุปข้อมูลที่ต้องใช้get : departure_station, destination_station, amount, departure_date(entry.get)
        member_id = self.cache["user"]["member_id"]
        train_id = self.cache["train_id"]
        bogie_id = self.cache["bogie_id"]
        departure_station = self.cache["departure_station"].get()
        destination_station = self.cache["destination_station"].get()
        error = body["error"]
        
        departure_time = self.cache["departure_time"]
        
        destination_time = self.cache["destination_time"]
        
        departure_date = self.cache["departure_date"].entry.get()
        
        choosed_seat_id_list = body["seats"]
        response = FrameController.fetch_choose_seat(member_id, train_id, bogie_id, departure_station, destination_station
                                                     , departure_time, destination_time, departure_date, choosed_seat_id_list)
        if isinstance(response, dict) and  response.get("error"):
            error.config(text=f"Choosed seat/seats in already booked.")
            return "error"
        
        self.cache["reservation_id"] = response[0]["reservation_id"]
        self.cache["reserved_seats"] = response[1]["seats"]
        self.cache["price"] = response[2]["price"]
        self.cache["meals"] = response[3]["meals"]
        coupon_list = FrameController.fetch_coupon(self.cache["user"]["member_id"])
        self.cache["coupon_list"] = coupon_list
        return "pass"
    

    def submit_req_bogie(self, body) :
        train_id = body["train_id"]
        bogie_id = body["bogie_id"]
        departure_time = self.cache["departure_time"]
        departure_date = self.cache["departure_date"].entry.get()

        result_seat_list = FrameController.fetch_choose_bogie(train_id, bogie_id, departure_time, departure_date)
        
        self.cache["bogie_id"] = bogie_id
        self.cache["available_seat_list"] = result_seat_list
         
        return result_seat_list
    
    def submit_logout(self):
        for data in self.cache.keys():
                self.cache[data] = None
        for frame in self.__frames.keys():
            if frame != "main":
                self.__frames[frame].destroy()
            else:
                self.__frames[frame].user_frame.destroy()
    def submit_login(self, body):
        username = body["username"].get()
        password = body["password"].get()
        error = body["error"]
        response = FrameController.fetch_login(username, password)
        if response == "Wrong Password or No Username":
            error.config(text="Wrong Password or No Username", foreground="red")
            return "error"
        else:
            self.cache["user"] = response
            return "success"
    def submit_cancel(self,body):
        ticket_id = body["ticket_id"]
        member_id = self.cache["user"]["member_id"]
        departure_time = body["departure_time"]
        date = body["departure_date"]
        error = body["error"]
        response = FrameController.fetch_cancel(ticket_id,member_id,departure_time,date)
        if response["response status"] == "too late":
            error.config(text="Too late to cancel", foreground="red")
            return
        elif response["response status"] == "delete success":
            self.__frames["ticket"].destroy()
            for ticket in self.cache["ticket_list"]:
                if ticket["ticket_ID"] ==  ticket_id:
                    self.cache["ticket_list"].remove(ticket)
            payload = {"go_to":"ticket"}
            self.set_page_state(payload)
            
    def submit_register(self, body):
        username = body["username"].get()
        name = body["name"].get()
        password = body["password"].get()
        confirm_password = body["confirm"].get()
        error = body["error"]
        response = self.validate("register",body)
        if response != "pass":
            return
        
        else :
            response = FrameController.fetch_register(username,name,password)
            if response == "Successful":
                error.config(text="Successful",foreground="green")
            elif response == "Username already exists.":
                error.config(text="Username already exists.",foreground="red")
    
    
    def submit_req_route(self, body):
        combo_departure = body["combo_departure"]
        combo_destination = body["combo_destination"]
        my_date = body["my_date"]
        entry_amount = body["entry_amount"]
        error = body.get("error")
        result_route_list = FrameController.fetch_choose_route(
            combo_departure, combo_destination, my_date, entry_amount
        )
        if not isinstance(result_route_list,list) and result_route_list.get("error"):
            error.config(text=result_route_list["error"],foreground="red")
            return "error"
        self.cache["route_list"] = result_route_list
        self.cache["departure_station"] = combo_departure
        self.cache["destination_station"] = combo_destination
        self.cache["departure_date"] = my_date
        self.cache["amount"] = entry_amount
        return result_route_list
    
    def submit_req_train(self, body):
        train_id = body["train_id"]
        departure_time = body["departure_time"]
        destination_time = body["destination_time"]
        result_bogie_list = FrameController.fetch_choose_train(train_id)
        self.cache["train_id"] = train_id
        self.cache["departure_time"] = departure_time
        self.cache["destination_time"] = destination_time
        return result_bogie_list
    
    def validate(self,method,body):
        if method == "train":
            departure = body["combo_departure"].get()
            destination = body["combo_destination"].get()
            my_date = body["my_date"].entry.get()
            error = body.get("error")
            amount = body["entry_amount"].get()

            try:
                my_date = datetime.strptime(my_date, '%Y-%m-%d').date()
            except ValueError:
                error.config(text="Invalid date", foreground="red")
                return "invalid"
            
            if departure == "" or destination == "" or my_date == "" or amount == "":
                error.config(text="Please fill in all fields", foreground="red")
                return "Please fill in all fields"
            elif departure == destination:
                error.config(text="Enter different stations.", foreground="red")
                return "same station"
            elif my_date < datetime.now().date():
                error.config(text="Invalid date", foreground="red")
                return "Invalid date"
            elif not amount.isdigit() or int(amount) <= 0:
                error.config(text="Invalid amount", foreground="red")
                return "Invalid amount"
            else:
                return "pass"
        elif method == "login":
            username = body["username"].get()
            password = body["password"].get()
            error = body["error"]
            if username == "" or password == "":
                error.config(text="Please fill in all fields", foreground="red")
                return "Please fill in all fields"
            else:
                return "pass"
        elif method == "register":
            username = body["username"].get()
            name = body["name"].get()
            password = body["password"].get()
            confirm = body["confirm"].get()
            error = body["error"]
            if username == "" or password == "" or  name == "" or confirm == "":
                error.config(text="Please fill in all fields", foreground="red")
                return "Please fill in all fields"
            elif password != confirm:
                error.config(text="Password do not match")
                return "Password do not match"
            else:
                return "pass"
    @staticmethod
    def fetch_payment(reservation_id,payment_method,coupon_id=None):
        data = {"reservation_id": reservation_id, "payment_method": payment_method, "coupon_id": coupon_id}
        data = json.dumps(data)
        requests.post("http://localhost:8000/pay",data)

    @staticmethod
    def fetch_coupon(member_id):
        response = requests.get("http://localhost:8000/coupon",params=({"member_id": member_id}))
        response = response.json()
        coupon_list = response["coupon"]
        return coupon_list
    @staticmethod
    def fetch_meal(reservation_id,total_price_by_adding_food_from_UI,meal_form):
        data = {"reservation_id":reservation_id,"total_price_by_adding_food_from_UI":total_price_by_adding_food_from_UI,"meal_form":meal_form}
        data = json.dumps(data)
        response = requests.post("http://localhost:8000/meal",data)
        return response.json()
    @staticmethod
    def fetch_choose_seat(member_id, train_id, bogie_id, 
                          departure_station, destination_station, departure_time,
                          destination_time, departure_date, choosed_seat_id_list) :
        data = {"member_id": member_id, "train_id": train_id, "bogie_id": bogie_id,
                "departure":departure_station, "destination": destination_station, "departure_time": departure_time,
                "destination_time": destination_time, "date": departure_date, "choosed_seat_id_list": choosed_seat_id_list}
        data = json.dumps(data)
        response = requests.post(
            "http://localhost:8000/seat", data)
        
        return response.json()
    
    @staticmethod
    def fetch_choose_bogie(train_id, bogie_id, departure_time, departure_date) :
        response = requests.get(
            "http://localhost:8000/bogie",
            params={
                "train_id": train_id,
                "bogie_id":bogie_id,
                "departure_time": departure_time,
                "date": departure_date
            }
        )
        result_seat_list = response.json()
        return result_seat_list
    
    @staticmethod
    def fetch_choose_train(train_id):

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
        response = requests.get("http://localhost:8000/root")
        stations_list = response.json()
        return stations_list
    
    @staticmethod
    def fetch_login(username, password):
        form = {"username":username, "password":password}
        response = requests.post(
            "http://localhost:8000/login",data=json.dumps(form))
        response = response.json()
        return response
    
    #! Edited: add fetch_register
    @staticmethod
    def fetch_register(username, name, password):
        form = {"username":username, "name":name, "password":password}
        response = requests.post(
            "http://localhost:8000/register",data=json.dumps(form))
        result_response = response.json()
        
        return result_response
    
    @staticmethod
    def fetch_ticket_list(member_id):
        response =requests.get("http://localhost:8000/view_ticket",params={"member_id":member_id})
        response = response.json()
        return response
    
    @staticmethod
    def fetch_cancel(ticket_id, member_id, departure_time, departure_date):
        form = {"member_id":member_id, "ticket_id":ticket_id, "departure_time":departure_time,"date":departure_date}
        response = requests.delete(
            "http://localhost:8000/cancel",data=json.dumps(form))
        result_response = response.json()
        return result_response
    @staticmethod
    def fetch_choose_route(combo_departure, combo_destination, my_date, entry_amount):
        departure = combo_departure.get()
        destination = combo_destination.get()
        choose_date = my_date.entry.get()
        amount = entry_amount.get()

        choose_date = datetime.strptime(choose_date, "%Y-%m-%d")

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

class App(tk.Tk) :
    def __init__(self) :
        super().__init__()
        
        self.title("Ticket Reservation System")
        self.geometry("1200x600")
        self.resizable(0, 0)
        
        
if __name__ == "__main__" :
    app = App()
    FrameController(app)
    
    app.mainloop()