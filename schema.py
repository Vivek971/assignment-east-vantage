from pydantic import BaseModel,Field
from typing import Optional

class PlaceBase(BaseModel):
    address : str
    latitude : float = Field(...,ge=-90,le=90,description="Latitude in degrees, between -90 and 90")
    longitude : float = Field(...,ge=-180,le=180,description="Longitude in degrees, between -180 and 180")

class PlaceCreate(PlaceBase):
    pass

class PlaceUpdate(BaseModel):
    address: Optional[str] = Field(None, min_length=1, max_length=100)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    


class PlaceResponse(PlaceBase):
    id : int

    class Config:
        from_attributes = True


class NearbyPlaceQuery(BaseModel):
    latitude : float = Field(...,ge=-90,le=90,description="Latitude in degrees, between -90 and 90")
    longitude : float = Field(...,ge=-180,le=180,description="Longitude in degrees, between -180 and 180")
    distance_km : float = Field(...,ge=0,le=1000,description="Radius in kilometers, between 0 and 1000")
    limit : int = Field(10,ge=1,le=100,description="Maximum number of results, between 1 and 100")



class NearbyPlace(PlaceResponse):
    distance_km : float

class NearByPlaceList(BaseModel):
    places : list[NearbyPlace]





    