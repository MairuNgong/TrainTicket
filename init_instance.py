from init_class import TicketReservationSystem, Member, Station, Train, Bogie, Seat, Reminder, Route, Meal
from datetime import time
from init_class import *

# * main
system = TicketReservationSystem()

# * init member
member1 = Member("Kim","001","kim123")
member2 = Member("Boat","002","boat123")
# * init station
A_station = Station("A")
B_station = Station("B")
C_station = Station("C")
D_station = Station("D")
station_list = [A_station, B_station, C_station, D_station]

# * init train
train001 = Train("T001")
train002 = Train("T002")

# * init bogie
bogie001 = Bogie("B001")
bogie002 = Bogie("B002")
bogie_train001 = [bogie001, bogie002]

bogie003 = Bogie("B003")
bogie004 = Bogie("B004")
bogie_train002 = [bogie003, bogie004]

# * init seat
seat001 = Seat("S001")
seat002 = Seat("S002")
seat003 = Seat("S003")
seat004 = Seat("S004")
seat005 = Seat("S005")
seat_bogie001 = [seat001, seat002, seat003, seat004, seat005]

seat006 = Seat("S006")
seat007 = Seat("S007")
seat008 = Seat("S008")
seat009 = Seat("S009")
seat010 = Seat("S0010")
seat_bogie002 = [seat006, seat007, seat008, seat009, seat010]

seat011 = Seat("S011")
seat012 = Seat("S012")
seat013 = Seat("S013")
seat014 = Seat("S014")
seat015 = Seat("S015")

seat_bogie003 = [seat011, seat012, seat013, seat014, seat015]

seat016 = Seat("S016")
seat017 = Seat("S017")
seat018 = Seat("S018")
seat019 = Seat("S019")
seat020 = Seat("S020")

seat_bogie004 = [seat016, seat017, seat018, seat019, seat020]

# Define the reminders for route 1
route1_station_a = Reminder(A_station, time(0, 0))
route1_station_b = Reminder(B_station, time(3, 0))
route1_station_c = Reminder(C_station, time(6, 0))
route1_station_d = Reminder(D_station, time(9, 0))

# Define the reminders for route 2
route2_station_d = Reminder(D_station, time(12, 0))
route2_station_c = Reminder(C_station, time(15, 0))
route2_station_b = Reminder(B_station, time(18, 0))
route2_station_a = Reminder(A_station, time(21, 0))

# Define the reminders for route 3
route3_station_a = Reminder(A_station, time(12, 0))
route3_station_b = Reminder(B_station, time(15, 0))
route3_station_c = Reminder(C_station, time(18, 0))
route3_station_d = Reminder(D_station, time(21, 0))

# Define the reminders for route 4
route4_station_d = Reminder(D_station, time(0, 0))
route4_station_c = Reminder(C_station, time(3, 0))
route4_station_b = Reminder(B_station, time(6, 0))
route4_station_a = Reminder(A_station, time(9, 0))

station_route1 = [
    route1_station_a, route1_station_b, route1_station_c, route1_station_d
]

station_route2 = [
    route2_station_d, route2_station_c, route2_station_b, route2_station_a
]

station_route3 = [
    route3_station_a, route3_station_b, route3_station_c, route3_station_d
]

station_route4 = [
    route4_station_d, route4_station_c, route4_station_b, route4_station_a
]

# *init route
route1 = Route(train001, station_route1, "forward")
route2 = Route(train001, station_route2, "backward")
route3 = Route(train002, station_route3, "forward")
route4 = Route(train002, station_route4, "backward")

# *add route
system.add_route_list(route1)
system.add_route_list(route2)
system.add_route_list(route3)
system.add_route_list(route4)

# *add member
system.add_member_list(member1)
system.add_member_list(member2)
# * fill data

for seat in seat_bogie001:
    bogie001.add_seat(seat)

for seat in seat_bogie002:
    bogie002.add_seat(seat)

for seat in seat_bogie003:
    bogie003.add_seat(seat)

for seat in seat_bogie004:
    bogie004.add_seat(seat)

for bogie in bogie_train001:
    train001.add_bogie(bogie)

for bogie in bogie_train002:
    train002.add_bogie(bogie)

food1 = Meal("M001", 50)
food2 = Meal("M002", 60)
food3 = Meal("M003", 70)
food4 = Meal("M004", 80)

system.add_meal(food1)
system.add_meal(food2)
system.add_meal(food3)
system.add_meal(food4)