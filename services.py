import math
from sqlalchemy.orm import Session
from models import Place
from schema import PlaceCreate,NearbyPlaceQuery,PlaceUpdate
from utils import bounding_box,haversine


# Create place
def create_place(db: Session,place_data: PlaceCreate):

    # check if same coordinates already exist
    existing_place = db.query(Place).filter(
        Place.latitude == place_data.latitude,
        Place.longitude == place_data.longitude
    ).first()

    if existing_place:
        return existing_place
    
    place = Place(**place_data.dict())
    db.add(place)
    db.commit()
    db.refresh(place)
    return place


def get_place(db: Session, place_id: int):

    return db.query(Place).filter(
        Place.id == place_id
    ).first()

def get_places(db: Session, skip: int = 0, limit: int = 100):

    places =  db.query(Place)\
        .offset(skip)\
        .limit(limit)\
        .all()
    
    return places


def update_place(
    db: Session,
    place_id: int,
    place_data: PlaceUpdate
):

    place = db.query(Place).filter(
        Place.id == place_id
    ).first()

    if not place:
        return None

    update_data = place_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(place, key, value)

    db.commit()
    db.refresh(place)

    return place

def delete_place(db: Session, place_id: int):

    place = db.query(Place).filter(
        Place.id == place_id
    ).first()

    if not place:
        return None

    db.delete(place)
    db.commit()

    return place

def find_nearby_places(db: Session, query: NearbyPlaceQuery):

    lat_min, lat_max, lon_min, lon_max = bounding_box(
        query.latitude,
        query.longitude,
        query.distance_km
    )

    candidates = db.query(Place).filter(
        Place.latitude.between(lat_min, lat_max),
        Place.longitude.between(lon_min, lon_max)
    ).all()

    results = []

    for place in candidates:

        distance = haversine(
            query.latitude,
            query.longitude,
            place.latitude,
            place.longitude
        )

        if distance <= query.distance_km:
            results.append({
                "id": place.id,
                "address": place.address,
                "latitude": place.latitude,
                "longitude": place.longitude,
                "distance_km": distance
            })

    results.sort(key=lambda x: x["distance_km"])

    return results[: query.limit]