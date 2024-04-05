from typing import List, Dict
import uvicorn
from fastapi import FastAPI, Query, Path, Form
import json
from datetime import date, time, datetime, timedelta
from init_instance import system

#! all id have to change to uuid
app = FastAPI()

if __name__ == "__main__" :
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info")

@app.get("/route")
async def choose_route(departure: str, destination: str, choose_date: datetime, amount: int):
    result_route = system.choose_route(departure, destination, choose_date, amount)
    return result_route

@app.get("/train")
async def choose_train(train_id: str, departure: str, destination: str, departure_time: time, destination_time: time, date: datetime, amount: int):
    bogies = system.choose_train(train_id, departure, destination, departure_time, destination_time, date, amount)
    return bogies

@app.get("/bogie")
async def choose_bogie(train_id: str, bogie_id: str, departure: str, destination: str, departure_time: time, destination_time: time, date: datetime, amount: int):
    seats = system.choose_bogie(system, train_id, bogie_id, departure, destination, departure_time, destination_time, date, amount)
    return seats

@app.post("/seat")
async def choose_seat(member: str, train_id: str, bogie_id: str, departure: str, destination: str, departure_time: time, destination_time: time, date: datetime, seat_list: List[str] = Query(...)):
    reservation = system.choose_seat(member,train_id, bogie_id, departure, destination, departure_time, destination_time, date, seat_list)
    return reservation

@app.post("/meal")
async def choose_meal(reservation_id: str, total_price_by_adding_food_from_UI: int, meal_form: List[Dict[str, str]] = Form(...)):
    summary_data = system.choose_meal(reservation_id, total_price_by_adding_food_from_UI, meal_form)
    return summary_data

