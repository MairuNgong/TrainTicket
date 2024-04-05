class Ticket:
    __ID = 0
    def __init__(self, reservation, seat):
        self.__ticket_id = str(Ticket.__ID)
        Ticket.__ID += 1
        self.__reservation_id = reservation.get_reservation_id()
        self.__date = seat.get_date()
        self.__departure_station = reservation.get_departure_station()
        self.__destination_station = reservation.get_destination_station()
        self.__departure_time = seat.get_departure_time()
        self.__destination_time = seat.get_destination_time()
        self.__train_id = reservation.get_train().get_train_id()
        self.__bogie_id = reservation.get_bogie().get_bogie_id()
        self.__seat_id = seat.get_seat_id()

    def get_date(self):
        return self.__date

    def get_departure_station(self):
        return self.__departure_station.get_station_name()

    def get_destination_station(self):
        return self.__destination_station.get_station_name()

    def get_departure_time(self):
        return self.__departure_time

    def get_destination_time(self):
        return self.__destination_time

    def get_train_id(self):
        return self.__train_id

    def get_bogie_id(self):
        return self.__bogie_id

    def get_seat_id(self):
        return self.__seat_id
    
    def get_reservation_id(self) :
        return self.__reservation_id
    
    def get_ticket_id(self) :
        return self.__ticket_id
    