class Route:
    def __init__(self, train, reminder_list, route_type):
        self.__train = train
        self.__reminder_list = reminder_list
        self.__route_type = route_type

    def get_reminder_list(self):
        return self.__reminder_list

    def get_train(self):
        return self.__train