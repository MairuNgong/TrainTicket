from .Payment import Payment

class PromptPay(Payment):
    def __init__(self,promptpay_value):
        super().__init__()
        self.__promptpay_id = promptpay_value[0]
    def get_promptpay_id(self):
        return self.__promptpay_id