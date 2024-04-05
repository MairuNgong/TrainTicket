from datetime import date, datetime, timedelta
from .Reservation import Reservation
from .SeatInUse import SeatInUse
from .Payment import Payment
from .PromptPay import PromptPay
from .CreditCard import CreditCard
from .MealReservation import MealReservation
from .Ticket import Ticket
from .Member import Member
class TicketReservationSystem:
    __member_list = []
    __route_list = []
    __reservation_list = []
    __coupon_list = []
    __station_list = []
    __meal_list = []
    
    # NOTE #!fill data to controller 
    def add_member_list(self, member):
        self.__member_list.append(member)
        
    def add_station_list(self,staion):
        self.__station_list.append(staion)
        
    def add_station_list(self, station):
        self.__station_list.append(station)
        
    def add_route_list(self, route):
        self.__route_list.append(route)
        
    def add_reservation(self, reservation): 
        self.__reservation_list.append(reservation)
 
    def add_meal(self, meal) :
        self.__meal_list.append(meal)
    
    def add_coupon(self,coupon):
        self.__coupon_list.append(coupon)

    def add_coupon_available(self, member_id):
        available_coupon = self.__coupon_list
        member = self.search_member_from_id(member_id)
        for coupon in member.get_coupon_list():
            if coupon in available_coupon:
                available_coupon.remove(coupon) 
        result = []
        for coupon in available_coupon:
              result.append({"coupon_id":coupon.get_coupon_id(),"discount":coupon.get_discount()})
        return result    
                

    # NOTE #!response methode
    def register(self,username,name,password):
        if self.search_member_from_username(username) !=  None:
                return "Username already exists."
        self.add_member_list(Member(username, name, password))
        return "Successful"
    
    def login(self, username, password):
        user = self.search_member_from_username(username)
        if user !=  None and password == user.get_password():
            format_user = {"name":user.get_name(),"username":user.get_username(),"member_id":user.get_member_id()}
            return format_user
        else:
            return "Wrong Password or No Username"

    def get_all_station(self) :
        station_list_format = []
        station_list = self.get_station_list()
        for station in station_list :  
            station_list_format.append({"station name": station.get_station_name()})
        return station_list_format
        
    def choose_route(self, departure, destination, choose_date, amount):
        #*VALIDATE
        if amount <= 0 :
            return {"error": "invalid amount"}
        if self.search_station_from_staion_name(departure) == None or self.search_station_from_staion_name(destination) == None:
            return {"error": "invalid station"}

        # *time is not matter if tomorrow
        if choose_date.date() > date.today():
            choose_date = choose_date.replace(hour=0, minute=0)
        else:
            # *time is matter
            choose_date = choose_date.replace(hour=datetime.now().hour, minute=datetime.now().minute)
        result_routes = self.search_route(departure, destination, choose_date.time())
        format_routes = []
        #* get departure time and destination time in each route
        for route in result_routes:
            destination_time = -1
            departure_time = -1
            for reminder in route.get_reminder_list():
                if reminder.get_station().get_station_name() == departure:
                    departure_time = reminder.get_time()
                elif reminder.get_station().get_station_name() == destination:
                    destination_time = reminder.get_time()
            # * format the route to JSON
            format_routes.append({
                route.get_train().get_train_id(): {
                    "departure": departure,
                    "destination": destination,
                    "departure_time": departure_time,
                    "destination_time": destination_time,
                    "date": choose_date.date(),
                    "amount": amount
                }
            })
        return format_routes
    
    def choose_train(self,train_id):
        result_bogie_list = self.search_bogie_list_from_train_id(train_id)
        if result_bogie_list == []:
            return  {"error":"invalid train id"}
        format_bogies = []
        for bogie in result_bogie_list:
            format_bogies.append({
                bogie.get_bogie_id(): {"train_id": train_id}
            })
        return format_bogies
    
    def choose_bogie(self, train_id, bogie_id, departure_time, date):
        result_seat_list = self.search_available_seat_list(train_id, bogie_id, departure_time, date)
        if result_seat_list == []:
            return {"error":"invalid train id"}
        elif result_seat_list == None:
            return {"error":"invalid bogie id"}
        
        format_seats = []
        for seat in result_seat_list:
            format_seats.append({
                "seat_no": seat.get_seat_id()
            })
        return format_seats

    def choose_seat(self,member_id, train_id, bogie_id, departure, destination, departure_time, destination_time, date, seat_id_list):
        #* VALIDATE
        try:
            departure_time = datetime.strptime(departure_time, '%H:%M:%S').time()
            destination_time = datetime.strptime(destination_time, '%H:%M:%S').time()
            date = datetime.strptime(date, '%Y-%m-%d')
            member = self.search_member_from_id(member_id)
            if member == None:
                return {"error":"invalid member id"}
            result_seat_list = self.search_available_seat_list(train_id, bogie_id, departure_time, date)
            if result_seat_list == []:
                return {"error":"invalid train id"}
            elif result_seat_list == None:
                return {"error":"invalid bogie id"}
            if self.search_station_from_staion_name(departure) == None or self.search_station_from_staion_name(destination) == None:
                return {"error": "invalid staion"}
            seat_cnt = 0
            for seat_id in seat_id_list:
                for available_seat in result_seat_list:
                    if seat_id == available_seat.get_seat_id():
                        seat_cnt+=1
                        break
            if seat_cnt < len(seat_id_list):
                return {"error": "invalid seat id"}
        except ValueError:
            return {"error":"format is incorrect."}
        
        
        init_time = datetime.now().time()
        reservation = self.create_reservation(member,departure, destination, departure_time, destination_time, seat_id_list,date, train_id, bogie_id, init_time)
        self.add_reservation(reservation)
        format_reservation = []
        format_reservation.append({"reservation_id" : reservation.get_reservation_id()})
        seat_in_use_list = []
        for seat in reservation.get_seat_in_use_list():
            seat_in_use_list.append(seat.get_seat_id())
        format_reservation.append({"seats" : seat_in_use_list})
        format_reservation.append({"price" : reservation.get_price()})
        meal_list = []
        for meal in self.get_meal_list():
            meal_list.append({meal.get_meal_id(): meal.get_price()})
        format_reservation.append({"meals" : meal_list})
        return format_reservation

    
    def choose_meal(self, reservation_id, total_price_by_adding_food_from_UI, meal_form) :
        adding_price = self.calcurate_price_from_choosing_meal(meal_form)
        reserved_meal_list = self.prepare_list_of_reserved_meal(meal_form)
        reservation = self.search_reservation_by_id(reservation_id)
        reservation.update_price_from_choosing_meal(total_price_by_adding_food_from_UI, adding_price)
        reservation.add_reserved_meal_list(reserved_meal_list)
        seat_in_use_list = []
        for seat in reservation.get_seat_in_use_list():
            seat_in_use_list.append(seat.get_seat_id())
        format_summary = {
                    "train_id": reservation.get_train().get_train_id(),
                    "bogie_id": reservation.get_bogie().get_bogie_id(),
                    "seat": seat_in_use_list,
                    "departure": reservation.get_departure_station().get_station_name(),
                    "destination": reservation.get_destination_station().get_station_name(),
                    "departure_time": reservation.get_seat_in_use_list()[0].get_departure_time(),
                    "destination_time": reservation.get_seat_in_use_list()[0].get_destination_time(),
                    "date": reservation.get_departure_date(),
                    "reservation_id": reservation.get_reservation_id(),
                    "price": reservation.get_price()
            }
        return format_summary
    
    def pay(self,reservation_id, payment_method, coupon_id):
        reservation = self.search_reservation_by_id(reservation_id)
        for key in payment_method.keys():
            if key == "promptpay":
                payment = PromptPay(payment_method[key])
            elif key == "credit_card":
                payment = CreditCard(payment_method[key])
        if coupon_id != None: 
            coupon = self.search_coupon_by_coupon_id(coupon_id)
            payment.apply_coupon(coupon)
            reservation.get_reserver().add_coupon(coupon)
        reservation.add_payment(payment)

        ticket_list = self.create_ticket_list(reservation)
        member = reservation.get_reserver()
        for ticket in ticket_list:
            member.add_ticket(ticket)
        format_ticket_list = []
        for ticket in ticket_list:
            format_ticket_list.append(
                {
                    "reservation_ID" : reservation_id,
                    "ticket_ID" : ticket.get_ticket_id(),
                    "seat_ID" : ticket.get_seat_id(),
                    "bogie_ID" : ticket.get_bogie_id(),
                    "train_ID": ticket.get_train_id(),
                    "date": ticket.get_date(),
                    "departure_station": ticket.get_departure_station(),
                    "destination_station": ticket.get_destination_station(),
                    "departure_time": ticket.get_departure_time(),
                    "destination_time": ticket.get_destination_time()
                }
            )
        return format_ticket_list
    
    def view_ticket(self, member_id) :
        member = self.search_member_from_id(member_id)
        ticket_of_member_list = []
        for ticket in member.get_ticket_list():
            ticket_of_member_list.append(
                {
                    "reservation_ID" : ticket.get_reservation_id(),
                    "ticket_ID" : ticket.get_ticket_id(),
                    "seat_ID" : ticket.get_seat_id(),
                    "bogie_ID" : ticket.get_bogie_id(),
                    "train_ID": ticket.get_train_id(),
                    "date": ticket.get_date(),
                    "departure Station": ticket.get_departure_station(),
                    "destination Station": ticket.get_destination_station(),
                    "departure Time": ticket.get_departure_time(),
                    "destination Time": ticket.get_destination_time()
                }
            )
        return ticket_of_member_list
    3
    def cancel(self, member_id, ticket_id,departure_time,date) :
        departure_time = datetime.strptime(departure_time, '%H:%M:%S').time()
        date = datetime.strptime(date, '%Y-%m-%d')
        departure_datetime = datetime.combine(date, departure_time)
        current_datetime = datetime.now()
        time_limit = (departure_datetime - timedelta(minutes=60))
        if current_datetime  > time_limit:
            return {"response status": "too late"}
        member = self.search_member_from_id(member_id)
        result_ticket = member.search_ticket_by_id(ticket_id)                                                                                          
        if result_ticket == None : return {"response status": "ticket not found"}
        reservation_id = result_ticket.get_reservation_id()
        
        result_reservation = self.search_reservation_by_id(reservation_id)
        for seat_in_use in result_reservation.get_seat_in_use_list() :
            if seat_in_use.get_seat_id() == result_ticket.get_seat_id() :
                result_reservation.get_seat_in_use_list().remove(seat_in_use)
                member.get_ticket_list().remove(result_ticket)
                return {"response status": "delete success"}
        
    
    #NOTE #!prepare data methode
    def search_route(self, departure, destination, time):
        route_list = []
        for route in self.get_route_list():
            destination_index = -1
            departure_index = -1
            for reminder in route.get_reminder_list():
                if (reminder.get_station().get_station_name() == departure and reminder.get_time() >= time):
                    departure_index = route.get_reminder_list().index(reminder)
                elif (reminder.get_station().get_station_name() == destination and reminder.get_time() >= time):
                    destination_index = route.get_reminder_list().index(reminder)
            if (departure_index < destination_index and destination_index != -1 and departure_index != -1):
                route_list.append(route)
        return route_list
    
    def search_member_from_id(self, id):
        for member in self.__member_list:
            if member.get_member_id() == id:
                return member
    def search_member_from_username(self, username):
        for  member in self.__member_list:
            if member.get_username() == username:
                return member
            
    def search_route_from_train_id(self,train_id):
        route_list = []
        for route in self.get_route_list():
            if route.get_train().get_train_id() == train_id:
                route_list.append(route)
        return route_list
    
    def search_station_from_staion_name(self,station_name):
        for station in self.__station_list:
            if station.get_station_name() == station_name:
                return station
            
    def search_coupon(self, payment):
        for each_coupon in self.get_coupon_list():
            if payment.coupon.id == each_coupon.id:
                payment.apply_coupon(payment)
                Reservation.add_payment(payment)

    # add
    def search_train_from_train_id(self, train_id):
        for route in self.__route_list:
            train = route.get_train()
            if train.get_train_id() == train_id : return train
            
    # add
    def search_bogie_from_bogie_id_and_train_id(self, train_id, bogie_id):
        # get_bogie_list_from_train_id
        bogie_list = self.search_bogie_list_from_train_id(train_id)
        if bogie_list == []:
            return bogie_list
        result_bogie = None
        for bogie in bogie_list:
            if bogie.get_bogie_id() == bogie_id:
                result_bogie = bogie
                break
        return result_bogie

    # add
    def prepare_reservation_list(self):
        for reservation in self.__reservation_list:
            if not reservation.is_paid() and not reservation.is_alive():
                self.__reservation_list.remove(reservation)
    # add
    def search_bogie_list_from_train_id(self, train_id):
        if self.search_train_from_train_id(train_id) == None:
            return  []
        result_bogie_list = [bogie for bogie in self.search_train_from_train_id(train_id).get_bogie_list()]
        return result_bogie_list
   
    def search_coupon_by_coupon_id(self,coupon_id):
        for coupon in self.__coupon_list:
            if coupon.get_coupon_id()==coupon_id:
                return coupon
    # add
    def search_available_seat_list(self, train_id, bogie_id, departure_time, date):
        available_seat_list = []
        bogie = self.search_bogie_from_bogie_id_and_train_id(train_id, bogie_id)
        if bogie == [] or bogie == None:
            return bogie
        seat_in_bogi_list = bogie.get_seat_list()
        self.prepare_reservation_list()
        prepared_reservation_list = self.__reservation_list
        for seat in seat_in_bogi_list:
            seat_available_state = True
            for reservation in prepared_reservation_list:
                for seat_in_use in reservation.get_seat_in_use_list():
                    if seat_in_use.get_seat_id() == seat.get_seat_id() and seat_in_use.get_destination_time() > departure_time and seat_in_use.get_date() == date.date():
                        seat_available_state = False
            if seat_available_state == True:
                available_seat_list.append(seat)
        return available_seat_list
    
    def search_reservation_by_id(self, reservation_id) :
        for reservation in self.__reservation_list :
            if reservation.get_reservation_id() == reservation_id : return reservation
    
    def calcurate_price_from_choosing_meal(self, meal_form) :
        adding_price = 0
        for meal in meal_form :
            for system_meal in self.__meal_list :
                if meal["meal_id"] == system_meal.get_meal_id() :
                    adding_price += system_meal.get_price() * int(meal["amount"])
        return adding_price

    def prepare_list_of_reserved_meal(self, meal_form) :
        reserved_meal_list = []
        for meal in meal_form :
            for system_meal in self.__meal_list :
                if meal["meal_id"] == system_meal.get_meal_id() :
                    reserved_meal_list.append(MealReservation(system_meal, meal["amount"]))
        return reserved_meal_list
    
    def det_station_list(self) :
        return self.__station_list

    #NOTE #!getter
    def get_route_list(self):
        return self.__route_list
    
    def get_reservation_list(self):
        return self.__reservation_list

    def get_station_list(self):
        return self.__station_list

    def get_coupon_list(self):
        return self.__coupon_list
    
    def get_meal_list(self):
        return self.__meal_list
    
    def get_coupon_list(self):
        return self.__coupon_list

    #NOTE #!creating new instance
    def create_reservation(self,reserver, departure_station, destination_station, departure_time, destination_time, choosed_seat_id_list,
                           date, train_id, bogie_id, init_time):  ##
        train = self.search_train_from_train_id(train_id)
        bogie = self.search_bogie_from_bogie_id_and_train_id(train_id, bogie_id)
        departure_station = self.search_station_from_staion_name(departure_station)
        destination_station = self.search_station_from_staion_name(destination_station)
        reservation = Reservation(reserver,departure_station, destination_station, date, train, bogie)
        reservation.set_expired_time(init_time)
        seat_in_use_list = self.create_seat_in_use_list(departure_time, destination_time, choosed_seat_id_list, date)
        reservation.add_seat_in_use(seat_in_use_list)
        route_list = self.search_route_from_train_id(train_id)
        reservation.add_price(route_list,departure_station,destination_station)
        return reservation

    def create_seat_in_use_list(self, departure_time, destnation_time, seat_id_list, date):
        seat_in_use_list = []
        for seat_id in seat_id_list:
            seat_in_use = SeatInUse(seat_id, departure_time, destnation_time, date)
            seat_in_use_list.append(seat_in_use)
        return seat_in_use_list

    def create_ticket_list(self, reservation):
        ticket_list = []
        for seat in reservation.get_seat_in_use_list():
            ticket_list.append(Ticket(reservation,seat))
        return ticket_list
    
    