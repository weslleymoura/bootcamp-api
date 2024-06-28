from src.database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, text, Float


class ApiCall(Base):
    
    __tablename__ = "api_call"

    id = Column(Integer,primary_key=True,nullable=False)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    res_is_region_covered = Column(Boolean, nullable=False)
    res_closest_center_id = Column(Integer, nullable=False)
    res_closest_center_distance_in_km = Column(Float, nullable=False)
    res_closest_center_lat = Column(Float, nullable=False)
    res_closest_center_lng = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))