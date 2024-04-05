class Seat:
    def __init__(self, seat_id):
        self.__seat_id = seat_id

    def get_seat_id(self):
        return self.__seat_id

    def get_seat_position(self):
        return self.__seat_position