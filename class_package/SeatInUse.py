from .Seat import Seat

class SeatInUse(Seat):
    def __init__(self, seat_id, departure_time, destination_time, date):
        super().__init__(seat_id)
        self.__departure_time = departure_time
        self.__destination_time = destination_time
        self.__date = date.date()

    # add
    def get_destination_time(self):
        return self.__destination_time
    def get_departure_time(self) :
        return self.__departure_time
    def get_date(self):
        return self.__date