from typing import Union
from enum import Enum

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


class Category(Enum):
    SPORT = "sport"
    KICHEN = "kitchen"


class Item(BaseModel):
    id: int
    name: str
    price: float
    count: int = 0
    category: Category


items_db = {
    0: Item(
        id=0,
        name="baseball",
        price=10.99,
        count=10,
        category=Category.SPORT,
    ),
    1: Item(
        id=1,
        name="brush",
        price=2.99,
        count=20,
        category=Category.KICHEN,
    ),
}

app = FastAPI()


@app.get("/items")
def get_items():
    return items_db


@app.get("/items/{id}")
def get_item_by_id(id: int):
    if id not in items_db.keys():
        raise HTTPException(404, f"Item with id {id}. does not find.")
    return items_db[id]


@app.post("/items")
def add_item_by_id(item: Item):
    if item.id in items_db.keys():
        raise HTTPException(400, f"Item id {item.id} already exists.")
    items_db.update({item.id: item})
    return {"added": item}


@app.put("/items/{id}")
def update_item(
    id: int,
    name: Union[str, None] = None,
    price: Union[float, None] = None,
    count: Union[int, None] = None,
    category: Union[Category, None] = None,
):
    if id not in items_db.keys():
        raise HTTPException(404, f"Item with id {id}. does not find.")
    if all(val is None for val in (name, price, count, category)):
        raise HTTPException(400, "No paramemter provided for update.")

    item = items_db[id]
    if name:
        item.name = name
    if price is not None:
        item.price = price
    if count is not None:
        item.count = count
    if category:
        item.category = category

    return {"updated": item}
