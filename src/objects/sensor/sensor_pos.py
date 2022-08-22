from objects.common_base import Base
from sqlalchemy import Column, BigInteger, String


class SensorPos(Base):
    __tablename__ = "sensor_pos"
    pos_id = Column(BigInteger, primary_key=True)
    pos_code = Column(String)
    pos_dtl = Column(String)
    pos_name = Column(String, nullable=False)
