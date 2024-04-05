
class Reminder:
    def __init__(self, station, arrive_time):
        self.__station = station
        self.__arrive_time = arrive_time

    def get_station(self):
        return self.__station

    def get_time(self):
        return self.__arrive_time