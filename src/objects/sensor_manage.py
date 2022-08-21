from common_base import Base
from sqlalchemy import Column, BigInteger, String


class SensorType(Base):
    __tablename__ = 'sensor_type'
    type_id = Column(BigInteger, primary_key=True)
    type_code = Column(String, nullable=False)
    type_color_code = Column(String, nullable=False)
    type_name = Column(String, nullable=False)
    unit = Column(String)
