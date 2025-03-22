import uvicorn
from fastapi import FastAPI, Query

app = FastAPI()

hotels = [
    {"id": 1, "title": "Сочи"},
    {"id": 2, "title": "Дубай"},
    {"id": 3, "title": "Шанхай"}
]

@app.get("/hotels")
def get_hotels(
    id: int | None = Query(None, description = "Идентификатор"),
    title: str | None = Query(None, description = "Название"),
):
    #return hotels
    return [hotel for hotel in hotels if (not id or hotel["id"] == id) and (not title or hotels["title"] == title)]

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host = "0.0.0.0",
        port = 8000,
        reload = True
    )