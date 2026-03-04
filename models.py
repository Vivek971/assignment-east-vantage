from sqlalchemy import Column,Integer,String,Float,Index
from database import Base


class Place(Base):
    __tablename__ = "places"

    id = Column(Integer,primary_key=True)
    address = Column(String,nullable=False)
    latitude = Column(Float,nullable=False)
    longitude = Column(Float,nullable=False)

    __table_args__ = (
        Index("idx_lat_lon","latitude","longitude"),
    )




