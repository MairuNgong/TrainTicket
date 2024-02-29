from datetime import date, time, datetime, timedelta
import uuid

class TicketReservationSystem:
    __member_list = []
    __route_list = []
    __reservation_list = []
    __payment_list = []
    __coupon_list = []
    __station_list = []
    __meal_list = []

    def add_member_list(self, member):
        self.__member_list.append(member)

    def choose_route(self, departure, destination, choose_date, amount):
        # *time is not matter if tomorrow
        if choose_date.date() > date.today():
            choose_date = choose_date.replace(hour=0, minute=0)
        else:
            # *time is matter
            choose_date = choose_date.replace(hour=datetime.now().hour, minute=datetime.now().minute)
        result_routes = self.search_route(departure, destination, choose_date.time())
        format_routes = []
        # * get departure time and destination time in each route
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
                    "Departure": departure,
                    "Destination": destination,
                    "Departure time": departure_time,
                    "Destination time": destination_time,
                    "Date": choose_date.date(),
                    "Amount": amount
                }
            })
        return format_routes
    
    def choose_train(self, train_id, departure, destination, departure_time, destination_time, date, amount):
        result_bogie_list = self.get_bogie_list_from_train_id(train_id)
        format_bogies = []
        for bogie in result_bogie_list:
            format_bogies.append({
                bogie.get_bogie_id(): {
                    "train_id": train_id,
                    "Departure": departure,
                    "Destination": destination,
                    "Departure time": departure_time,
                    "Destination time": destination_time,
                    "Date": date.date(),
                    "Amount": amount
                }
            })
        return format_bogies
    
    def choose_bogie(self, train_id, bogie_id, departure, destination, departure_time, destination_time, date, amount):
        result_seat_list = self.get_available_seat_list(train_id, bogie_id, departure_time, date)
        format_seats = []
        for seat in result_seat_list:
            format_seats.append({
                seat.get_seat_id(): {
                    "train_id": train_id,
                    "bogie_id": bogie_id,
                    "Departure": departure,
                    "Destination": destination,
                    "Departure time": departure_time,
                    "Destination time": destination_time,
                    "Date": date.date(),
                    "Amount": amount
                }
            })
        return format_seats
        
    ####
    def choose_seat(self,member_name, train_id, bogie_id, departure, destination, departure_time, destination_time, date, seat_list):
        init_time = datetime.now().time()
        reservation = self.create_reservation(member_name,departure, destination, departure_time, destination_time, seat_list,date, train_id, bogie_id, init_time)
        format_reservation = []
        format_reservation.append({"reservation_id" : reservation.get_reservation_id()})
        seat_list = []
        for seat in reservation.get_seat_inUse_list():
            seat_list.append(seat.get_seat_id())
        format_reservation.append({"Seats" : seat_list})
        format_reservation.append({"Price" : reservation.get_price()})
        meal_list = []
        for meal in self.get_meal_list():
            meal_list.append({meal.get_meal_id(): meal.get_price()})
        format_reservation.append({"Meals" : meal_list})
        return format_reservation

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
            
    def search_route_from_train_id(self,train_id):
        route_list = []
        for route in self.get_route_list():
            if route.get_train().get_train_id() == train_id:
                route_list.append(route)
        return route_list
    
    def search_bogie():
        pass

    def search_seat():
        pass

    def get_route_list(self):
        return self.__route_list

    def add_reservation(self, reservation):  ##
        self.__reservation_list.append(reservation)

    def create_reservation(self,reserver, departure_station, destination_station, departure_time, destination_time, seat_list,
                           date, train, bogie, init_time):  ##
        reservation = Reservation(reserver,departure_station, destination_station, seat_list, date, train, bogie)
        reservation.set_expired_time(init_time)
        reservation.create_seat_inuse(departure_time, destination_time, seat_list, date)
        reservation.add_price(self,train,departure_station,destination_station)
        self.add_reservation(reservation)
        return reservation

    def get_reservation():
        pass

    def get_station_list(self):
        return self.__station_list

    def add_station_list(self, station):
        self.__station_list.append(station)

    def add_route_list(self, route):
        self.__route_list.append(route)

    def get_coupon_list(self):
        return self.__coupon_list
    
    def get_meal_list(self):
        return self.__meal_list
    
    def search_coupon(self, payment):
        for each_coupon in self.get_coupon_list():
            if payment.coupon.id == each_coupon.id:
                payment.apply_coupon(payment)
                Reservation.add_payment(payment)

    def create_payment(self, payment_info):
        payment = Payment(payment_info)
        self.__payment_list.append(payment)
        self.search_coupon(payment)

    # add
    def get_train_from_train_id(self, train_id):
        for route in self.__route_list:
            train = route.get_train()
            if train.get_train_id() == train_id : return train
    #add
    def add_meal(self, meal) :
        self.__meal_list.append(meal)
    # add
    # ANCHOR add get_train_from_train_id
    def get_bogie_list_from_train_id(self, train_id):
        result_bogie_list = [bogie for bogie in self.get_train_from_train_id(train_id).get_bogie_list()]
        return result_bogie_list

    # add
    def get_bogie_from_bogie_id_and_train_id(self, train_id, bogie_id):
        # get_bogie_list_from_train_id
        bogie_list = self.get_bogie_list_from_train_id(train_id)
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
    def get_available_seat_list(self, train_id, bogie_id, departure_time, date):
        available_seat_list = []
        bogie = self.get_bogie_from_bogie_id_and_train_id(train_id, bogie_id)
        seat_in_bogi_list = bogie.get_seat_list()
        self.prepare_reservation_list()
        prepared_reservation_list = self.__reservation_list

        for seat in seat_in_bogi_list:
            seat_available_state = True
            for reservation in prepared_reservation_list:
                for seat_inUse in reservation.get_seat_inUse_list():
                    if seat_inUse.get_seat_id() == seat.get_seat_id() and seat_inUse.get_destination_time() > departure_time and seat_inUse.get_date() == date:
                        seat_available_state = False
            if seat_available_state == True:
                available_seat_list.append(seat)
        return available_seat_list
    
    def get_reservation_by_id(self, reservation_id) :
        for reservation in self.__reservation_list :
            if reservation.get_reservation_id == reservation_id : return reservation
    
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
                    reserved_meal_list.append(Meal_Reservation(system_meal, meal["amount"]))
        return reserved_meal_list
         

    def choose_meal(self, reservation_id, total_price_by_adding_food_from_UI, meal_form) :
        adding_price = self.calcurate_price_from_choosing_meal(meal_form)
        reserved_meal_list = self.prepare_list_of_reserved_meal(meal_form)
        reservation.update_price_from_choosing_meal(total_price_by_adding_food_from_UI, adding_price)
        reservation.add_reserved_meal_list(reserved_meal_list)
        reservation = self.get_reservation_by_id(reservation_id)
        seat_inUse_list = reservation.get_seat_inUse()
        format_summary = {
                    "train_id": reservation.get_train().get_train_id(),
                    "bogie_id": reservation.get_bogie().get_bogie_id(),
                    "seat": seat_inUse_list,
                    "Departure": reservation.get_departure_station().get_station_name(),
                    "Destination": reservation.get_destination_station().get_station_name(),
                    "Departure time": seat_inUse_list[0].get_departure_time(),
                    "Destination time": seat_inUse_list[0].get_destination_time(),
                    "Date": reservation.date,
                    "reservation_id": reservation.get_reservation_id(),
                    "price": reservation.get_price()
            }
        return format_summary



class Reservation:
    __ID = 0
    # add seat_inUse_list
    def __init__(self,reserver, departure_station, destination_station, seat_list, date, train, bogie):
        self.__reservation_id = str(Reservation.__ID)
        Reservation.__ID += 1
        self.__reserver = reserver
        self.__departure_station = departure_station
        self.__destination_station = destination_station
        self.__departure_date = date
        self.__train = train
        self.__bogie = bogie
        self.__price = 0
        self.__payment = None
        self.__expired_time = None
        self.__seat_inuse_list = []

    def get_departure_date(self) :
        return self.__departure_date
    
    def get_bogie(self) :
        return self.__bogie

    def get_train(self) :
        return self.__train
    
    def get_departure_station(self) :
        return self.__departure_station
    
    def get_destination_station(self) :
        return self.__destination_station
    
    def get_reservation_id(self) :
        return self.__reservation_id
    
    def get_price(self) :
        return self.__price

    def add_reserved_meal_list(self, reserved_meal_list) :
        self.__reserved_meal_list = reserved_meal_list
    
    def get_reserved_meal_list(self) :
        return self.__reserved_meal_list
                    
        
    def update_price_from_choosing_meal(self, adding_price, total_price_by_adding_food_from_UI) :
        if total_price_by_adding_food_from_UI == (self.__price + adding_price) : self.__price += adding_price
    
    def get_reserver(self) :
        return self.__reserver

    def add_price(self,system,train_id,departure_station,destination_station):
        route_list = system.search_route_from_train_id(train_id)
        travel_lenght = 0
        for route in route_list:
            destination_index = -1
            departure_index = -1
            for reminder in route.get_reminder_list():
                if (reminder.get_station().get_station_name() == departure_station):
                    departure_index = route.get_reminder_list().index(reminder)
                elif (reminder.get_station().get_station_name() == destination_station):
                    destination_index = route.get_reminder_list().index(reminder)
            if (departure_index < destination_index and destination_index != -1 and departure_index != -1):
                travel_lenght = (destination_index - departure_index)
        for seat in self.__seat_inuse_list:
            self.__price += (travel_lenght*20)

    def add_payment(self, payment):
        self.__payment = payment

    def is_paid(self):
        if self.__payment == None:
            return False
        else:
            return True

    # !! TIME
    def is_alive(self):
        if datetime.now().time() < self.__expired_time:
            return True
        else:
            return False

    ##
    def add_seat_in_use(self, new_seat_inuse):
        self.__seat_inuse_list.append(new_seat_inuse)

    ##
    def create_seat_inuse(self, departure_time, destnation_time, seat_list, date):
        for each_seat in seat_list:
            seat = Seat_inUse(each_seat, departure_time, destnation_time, date)
            self.add_seat_in_use(seat)

    # add !!TIME
    def set_expired_time(self, TIME: time):
        current_date = datetime.now().date()
        datetime_with_time = datetime.combine(current_date, TIME)
        self.__expired_time = (datetime_with_time + timedelta(minutes=5)).time()

    # add
    def get_seat_inUse_list(self):
        return self.__seat_inuse_list

    def create_ticket(self):
        pass

    def get_price(self):
        return self.__price
    
    def get_reservation_id(self):
        return self.__id

class User:
    def __init__(self):
        pass

    def login(self):
        pass


class Member(User):
    def __init__(self, name,id, password):
        self.__name = name
        self.__ticket_list = []
        self.__id = id
        self.__password = password

    def add_ticket(self, ticket):
        self.__ticket_list.append(ticket)

    def get_id(self):
        return self.__id

class Guest(User):
    def __init__(self):
        pass


class Ticket:
    def __init__(self, resevation):
        self.__resevation = resevation


class Seat:
    def __init__(self, seat_id):
        self.__seat_id = seat_id

    def get_seat_id(self):
        return self.__seat_id

    def get_seat_position(self):
        return self.__seat_position


# * change seat_inUse
class Seat_inUse(Seat):
    def __init__(self, seat_id, departure_time, destination_time, date):
        super().__init__(seat_id)
        self.__departure_time = departure_time
        self.__destination_time = destination_time
        self.__date = date

    # add
    def get_destination_time(self):
        return self.__destination_time
    def get_departure_time(self) :
        return self.__departure_time
    def get_date(self):
        return self.__date


# * change bogie
class Bogie:
    def __init__(self, bogie_id):
        self.__bogie_id = bogie_id
        self.__seat_list = []

    def add_seat(self, seat):
        self.__seat_list.append(seat)

    def get_seat_no():
        pass

    def make_available_seat():
        pass

    # add
    def get_bogie_id(self):
        return self.__bogie_id

    # add
    def get_seat_list(self):
        return self.__seat_list

    # add
    def get_destination_time(self):
        return self.__destination_time


# * change train
class Train:
    def __init__(self, train_id):
        self.__train_id = train_id
        self.__bogie_list = []

    def get_train_id(self):
        return self.__train_id

    def add_bogie(self, bogie):
        self.__bogie_list.append(bogie)

    def get_bogie_list(self):
        return self.__bogie_list


class Route:
    def __init__(self, train, reminder_list, route_type):
        self.__train = train
        self.__reminder_list = reminder_list
        self.__route_type = route_type

    def get_reminder_list(self):
        return self.__reminder_list

    def get_train(self):
        return self.__train


class Station:
    def __init__(self, station_name):
        self.__station_name = station_name

    def get_station_name(self):
        return self.__station_name


class Reminder:
    def __init__(self, station, arrive_time):
        self.__station = station
        self.__arrive_time = arrive_time

    def get_station(self):
        return self.__station

    def get_time(self):
        return self.__arrive_time


#change
class Meal:
    def __init__(self, meal_id, price):
        self.__meal_id = meal_id
        self.__price = price

    def get_meal_id(self) :
        return self.__meal_id
    def get_price(self) :
        return self.__price

class Coupon:
    def __init__(self, coupon_id, discount):
        self.__coupon_id = coupon_id
        self.__discount = discount

    def get_coupon(self):
        return self


class Payment:
    def __init__(self, method, coupon):
        self.__method = method
        self.__coupon = None

    def apply_coupon(self, payment):
        self.__coupon = payment.coupon

#add
class Meal_Reservation :
    def __init__(self, meal, amount_of_meal) :
        self.__meal = meal
        self.__amount_of_meal = amount_of_meal

    def get_meal(self) :
        return self.__meal
    
    def get_amount_of_meal(self) :
        return self.__amount_of_meal

    