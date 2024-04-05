class Payment:
    def __init__(self):
        self.__coupon = None

    def apply_coupon(self, coupon):
        self.__coupon = coupon
    def get_coupon(self):
        return self.__coupon