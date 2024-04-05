#add
class MealReservation :
    def __init__(self, meal, amount_of_meal) :
        self.__meal = meal
        self.__amount_of_meal = amount_of_meal

    def get_meal(self) :
        return self.__meal
    
    def get_amount_of_meal(self) :
        return self.__amount_of_meal