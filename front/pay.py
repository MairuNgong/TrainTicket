import tkinter as tk
import ttkbootstrap as ttk
from datetime import datetime
import requests
from ttkbootstrap.constants import *
import json

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
        
        credit_pass_lable = ttk.Label(self.credit_frame, text="Enter Credit Password")
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
        
        promptpay_entry = ttk.Entry(self.promptpay_frame, textvariable=self.credit_pass_input)
        promptpay_entry.grid(row=2, column=0, padx=10)
        
        balance_label = ttk.Label(self.promptpay_frame, text="balance")
        balance_label.grid(row=1, column=1, padx=10)
        
        balance_promptpay_entry = ttk.Entry(self.promptpay_frame, textvariable=self.balance_promptpay_input)
        balance_promptpay_entry.grid(row=2, column=1, padx=10)
        
        self.info_label = ttk.Label(self, bootstyle="danger", text="", font=aleart)
        
        self.submit_button = ttk.Button(self, text="SUBMIT", command=self.send_payload_payment, width=15)
        
        self.back_to_main_button = ttk.Button(self, text="BACK TO MAIN MENU", bootstyle="success", width=15)
        
    def raise_main_menu_button(self) :
        self.back_to_main_button.pack()
    
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
        
        if pay != self.controller.cache["price"] :
            self.raise_info_label_text_set("IMPROPER PAYMENT!!", "danger")
            return False
        
        else : return True 
        
            
    def send_payload_payment(self) :
        if self.radio_var.get() == "credit" :
            if self.validate_balance(self.balance_credit_input.get()) :           
                payment_payload = {"pagename":"paying", "body": self.balance_credit_input.get()}
                self.controller.set_page_state(payment_payload)
        elif self.radio_var.get() == "promptpay" :
            if self.validate_balance(self.balance_promptpay_input.get()) :
                payment_payload = {"pagename":"paying", "body": self.balance_promptpay_input.get()}
                self.controller.set_page_state(payment_payload)

class FrameController(ttk.Frame) :
    def __init__(self, root) :
        super().__init__(root)
        
        # self["bootstyle"] = SECONDARY
        self.pack(expand=True, fill=tk.BOTH)
        
        # self.selected_value = tk.StringVar()
        self.cache = {}
        self.cache["price"] = "100"
        
        
        self.__frames = {}
        self.__frames["paying"] = Pay_Page(self)
        self.set_page_state({"pagename": "paying", "body":""})
        self.cache["meals"] = [{'M001': 50}, {'M002': 60}, {'M003': 70}, {'M004': 80}]
        
    def set_page_state(self, payload):
        if payload["pagename"] == "main" :
            pass 
        elif payload["pagename"] == "paying" :
            response = self.submit_payment(payload["body"])
            if response["message"] == "seat_picked" :
                self.__frames["paying"].raise_info_label_text_set("PAYMENT FAIL: Someone just reserved the seat. That you have aleardy chosen.", "danger")
            elif response["message"] == "success" :
                self.__frames["paying"].drop_aleart()
                self.__frames["paying"].drop_submit_button()
                self.__frames["paying"].raise_info_label_text_set("SUCCESS", "success")
                self.__frames["paying"].raise_main_menu_button()
                
        for page in self.__frames.items() :
            page[1].pack_forget() if page[0] != payload["pagename"] else page[1].pack(expand=True, fill=tk.BOTH)
    
    def submit_payment(self, body) :
        return {"message": "success"}

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