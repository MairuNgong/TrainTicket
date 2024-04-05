from datetime import datetime, time, timedelta

class Reservation:
    __ID = 0
    def __init__(self,reserver, departure_station, destination_station, date, train, bogie):
        self.__reservation_id = str(Reservation.__ID)
        Reservation.__ID += 1
        self.__reserver = reserver
        self.__departure_station = departure_station
        self.__destination_station = destination_station
        self.__departure_date = date.date()
        self.__train = train
        self.__bogie = bogie
        self.__price = 0
        self.__payment = None
        self.__expired_time = None
        self.__seat_in_use_list = []
        
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

    def get_reserver(self) :
        return self.__reserver
    
    def get_reserved_meal_list(self) :
        return self.__reserved_meal_list
    
    def get_expire_time(self):
        return self.__expired_time
    # add
    def get_seat_in_use_list(self):
        return self.__seat_in_use_list
    
    
    #?###############################

    def add_reserved_meal_list(self, reserved_meal_list) :
        self.__reserved_meal_list = reserved_meal_list
    
    
    
    def update_price_from_choosing_meal(self, total_price_by_adding_food_from_UI, adding_price) :
        if total_price_by_adding_food_from_UI == (self.__price + adding_price) : self.__price += adding_price
    
    def update_price_from_coupon(self,coupon):
        discount = coupon.get_discount()
        if self.__price - discount < 0 :
            self.__price = 0
        else:
            self.__price -= discount
    def add_price(self,route_list,departure_station,destination_station):
        travel_lenght = 0
        for route in route_list:
            destination_index = -1
            departure_index = -1
            for reminder in route.get_reminder_list():
                if (reminder.get_station().get_station_name() == departure_station.get_station_name()):
                    departure_index = route.get_reminder_list().index(reminder)
                elif (reminder.get_station().get_station_name() == destination_station.get_station_name()):
                    destination_index = route.get_reminder_list().index(reminder)
            if (departure_index < destination_index and destination_index != -1 and departure_index != -1):
                travel_lenght = (destination_index - departure_index)
        for seat in self.__seat_in_use_list:
            self.__price += (travel_lenght*20)

    def add_payment(self, payment):
        self.__payment = payment
        if payment.get_coupon() != None:
            self.update_price_from_coupon(payment.get_coupon())
    def is_paid(self):
        if self.__payment == None:
            return False
        else:
            return True

    def is_alive(self):
        if datetime.now().time() < self.__expired_time:
            return True
        else:
            return False

    ##
    def add_seat_in_use(self, seat_in_use_list):
        self.__seat_in_use_list = seat_in_use_list

    # add !!TIME
    def set_expired_time(self, TIME: time):
        current_date = datetime.now().date()
        datetime_with_time = datetime.combine(current_date, TIME)
        self.__expired_time = (datetime_with_time + timedelta(minutes=5)).time()


    
