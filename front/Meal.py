import tkinter as tk
import ttkbootstrap as ttk
from datetime import datetime
import requests
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
import json

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

        meal_list = self.controller.cache['meals']
        for meal in meal_list:
                for menu,price in meal.items():

                    Meal_frame = ttk.LabelFrame(list_frame, bootstyle='info')
                    Meal_frame.pack()

                    meal_name = ttk.Label(Meal_frame,text=f"Menu: {menu} ",)
                    meal_name.pack(padx=10,side=LEFT, anchor=W )

                    meal_price = ttk.Label(Meal_frame,text=f'Price:{price} ')
                    meal_price.pack(padx=10,pady=20,side=LEFT,anchor=W)

                    meal_count = ttk.Spinbox(Meal_frame, from_=0, to=10, command=self.calculate_total_price)
                    meal_count.set(0)
                    meal_count.pack(side=RIGHT,anchor=E)
                    
                    self.all_spinbox.append({"meal": meal_count, "price": price, "meal_id": menu})
                    
        payload_back_button = {"go_to": "summation_from_meal"}
        back_button = ttk.Button(self, bootstyle="info", text="go back", command=lambda: self.controller.set_page_state(payload_back_button))
        back_button.place(x=10, y=500)

        submit_button = ttk.Button(list_frame,text='Submit',command=lambda: self.controller.set_page_state(self.create_paylod()))
        submit_button.pack()

        
class FrameController(ttk.Frame) :
    def __init__(self, root) :
        super().__init__(root)
        
        # self["bootstyle"] = SECONDARY
        self.pack(expand=True, fill=tk.BOTH)
        
        # self.selected_
        # value = tk.StringVar()
        self.cache = {}
        self.cache['meals'] = [{'M001': 50}, {'M002': 60}, {'M003': 70}, {'M004': 80}]
        self.cache["user"] = None
        
        self.__frames = {}
        self.__frames["main"] = Meal_Page(self)
        self.set_page_state({"pagename": "main"})
        
        
    def set_page_state(self, payload):
        for page in self.__frames.items() :
            page[1].pack_forget() if page[0] != payload["pagename"] else page[1].pack(expand=True, fill=tk.BOTH)


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