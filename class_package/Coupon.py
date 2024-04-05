class Coupon:
    def __init__(self, coupon_id, discount):
        self.__coupon_id = coupon_id
        self.__discount = discount

    def get_coupon_id(self):
        return self.__coupon_id
    def get_discount(self):
        return self.__discount