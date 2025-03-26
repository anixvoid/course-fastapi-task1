import uvicorn
from fastapi import FastAPI, Query, Body

app = FastAPI()

hotels = [
    {"id": 1, "title": "Сочи",   "name": "sochi"},
    {"id": 2, "title": "Дубай",  "name": "dubai"},
    {"id": 3, "title": "Шанхай", "name": "shanghai"}
]

@app.get("/hotels")
def get_hotels(
    hotel_id: int | None = Query(None, description = "Идентификатор"),
    title: str | None = Query(None, description = "Название"),
    name: str | None = Query(None, description = "Псевдоним"),
):

    return [hotel for hotel in hotels if (not hotel_id or hotel["id"] == hotel_id) and (not title or hotel["title"] == title) and (not name or hotel["name"] == name)]

@app.post("/hotels")
def create_hotel(
    title: str = Body(embed=True), #embed=True - передача параметра в формате json
    name: str = Body(embed=True) #embed=True - передача параметра в формате json
):
    global hotels

    hotel = {
        "id": hotels[-1]["id"] + 1,
        "title": title,
        "name": name,
    }
    hotels.append(hotel)

    return {
        "status": "OK",
        "id": hotel["id"]
    }

@app.delete("/hotels/{hotel_id}")
def delete_hotel(
    hotel_id: int
):
    global hotels
    hotels = list([hotel for hotel in hotels if hotel["id"] != hotel_id])
    return {
        "status": "OK", 
        "count": len(hotels)
    }

@app.put("/hotels/{hotel_id}")
def update_hotel(
    hotel_id: int,
    title: str,
    name: str
):
    global hotels
    for i, hotel in enumerate(hotels):
        if hotel["id"] == hotel_id:
            hotels[i] = {
                "id":    hotel_id, 
                "title": title,
                "name":  name
            }

            return {
                "status": "OK", 
                "count": len(hotels)
            }

    return {
        "status": "NOK", 
        "message": "Hotel not found"
    }

@app.patch("/hotels/{hotel_id}")
def patch_hotel(
    hotel_id: int,
    title: str | None = None,
    name: str | None = None
):
    global hotels
    for i, hotel in enumerate(hotels):
        if hotel["id"] == hotel_id:
            if title:
                hotel["title"] = title

            if name:
                hotel["name"] = name

            return {
                "status": "OK", 
                "count": len(hotels)
            }

    return {
        "status": "NOK", 
        "message": "Hotel not found"
    }
    


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host = "0.0.0.0",
        port = 8000,
        reload = True
    )