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