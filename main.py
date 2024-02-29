from typing import List
import uvicorn
from fastapi import FastAPI, Query, Path
import json
from datetime import date, time, datetime, timedelta
from init_instance import system

#! all id have to change to uuid
app = FastAPI()

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info")

@app.get("/route")
async def choose_route(member: str, departure: str, destination: str, choose_date: datetime, amount: int):
    member = system.search_member_from_name(member)
    result_route = member.choose_route(system,departure, destination, choose_date, amount)
    return result_route

@app.get("/train")
async def choose_train(member: str, train_id: str, departure: str, destination: str, departure_time: time, destination_time: time, date: datetime, amount: int):
    member = system.search_member_from_name(member)
    bogies = member.choose_train(system,train_id, departure, destination, departure_time, destination_time, date, amount)
    return bogies

@app.get("/bogie")
async def choose_bogie(member: str, train_id: str, bogie_id: str, departure: str, destination: str, departure_time: time, destination_time: time, date: datetime, amount: int):
    member = system.search_member_from_name(member)
    seats = member.choose_bogie(system, train_id, bogie_id, departure, destination, departure_time, destination_time, date, amount)
    return seats

@app.post("/seat")
async def choose_seat(member: str, train_id: str, bogie_id: str, departure: str, destination: str, departure_time: time, destination_time: time, date: datetime, seat_list: List[str] = Query(...)):
    member = system.search_member_from_name(member)
    reservation = member.choose_seat(system,member.get_name(),train_id, bogie_id, departure, destination, departure_time, destination_time, date, seat_list)
    return reservation