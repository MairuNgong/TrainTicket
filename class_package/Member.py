from .User import User

class Member(User):
    __ID = 0
    def __init__(self,username, member_name, password):
        self.__username = username
        self.__member_name = member_name
        self.__ticket_list = []
        self.__member_id = str(Member.__ID)
        Member.__ID += 1
        self.__password = password
        self.__coupon_list = []

    def add_ticket(self, ticket):
        self.__ticket_list.append(ticket)

    def get_name(self):
        return self.__member_name
    def get_username(self):
        return self.__username
    
    def get_member_id(self):
        return self.__member_id
    def get_coupon_list(self):
        return self.__coupon_list
    def add_coupon(self,coupon):
        self.__coupon_list.append(coupon)
    def get_ticket_list(self) :
        return self.__ticket_list
    def get_password(self):
        return self.__password
    def search_ticket_by_id(self, ticket_id) :
        for ticket in self.__ticket_list :
            if ticket.get_ticket_id() == ticket_id :
                return ticket