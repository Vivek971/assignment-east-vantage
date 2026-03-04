from fastapi import FastAPI,Depends,HTTPException
from database import SessionLocal,engine
from models import Base
from typing import List
from sqlalchemy.orm import Session
from schema import NearbyPlaceQuery,NearByPlaceList,PlaceCreate,PlaceResponse,PlaceUpdate
import services as place_service
from request_logger import RequestLoggingMiddleware



app = FastAPI()

Base.metadata.create_all(bind=engine)

app.add_middleware(RequestLoggingMiddleware)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health")
def health_check():
    return {"status":"ok"}

@app.get("/", response_model=List[PlaceResponse])
def get_places(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):

    return place_service.get_places(db, skip, limit)


@app.get("/{place_id}", response_model=PlaceResponse)
def get_place(
    place_id: int,
    db: Session = Depends(get_db)
):

    place = place_service.get_place(db, place_id)

    if not place:
        raise HTTPException(
            status_code=404,
            detail="Place not found"
        )

    return place

@app.post("/", response_model=PlaceResponse)
def create_place(
    place: PlaceCreate,
    db: Session = Depends(get_db)
):

    return place_service.create_place(db, place)

@app.put("/{place_id}", response_model=PlaceResponse)
def update_place(
    place_id: int,
    place_data: PlaceUpdate,
    db: Session = Depends(get_db)
):

    place = place_service.update_place(
        db,
        place_id,
        place_data
    )

    if not place:
        raise HTTPException(
            status_code=404,
            detail="Place not found"
        )

    return place

@app.post("/places/nearby",response_model=NearByPlaceList)
def get_nearby_places(
    query: NearbyPlaceQuery,
    db: Session = Depends(get_db)
    
):
    results = place_service.find_nearby_places(db, query)

    return {"places":results}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)