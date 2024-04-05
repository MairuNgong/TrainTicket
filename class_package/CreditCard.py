from .Payment import Payment

class CreditCard(Payment):
    def __init__(self,credit_card_value):
        super().__init__()
        self.__credit_card_id = credit_card_value[0]
        self.__security_code = credit_card_value[1]
    def get_credit_card_id(self):
        return self.__credit_card_id
    def get_security_code(self):
        return self.__security_code