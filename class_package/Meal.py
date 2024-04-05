#change
class Meal:
    def __init__(self, meal_id, price):
        self.__meal_id = meal_id
        self.__price = price

    def get_meal_id(self) :
        return self.__meal_id
    def get_price(self) :
        return self.__price