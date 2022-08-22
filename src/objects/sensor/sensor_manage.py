from objects.common_base import Base
from sqlalchemy import Column, BigInteger, Integer, Float, ForeignKey


class SensorManage(Base):
    __tablename__ = "sensor_manage"
    ss_id = Column(BigInteger, primary_key=True)
    range_type = Column(Integer)
    rstart = Column(Float, nullable=False)
    rlev1 = Column(Float, nullable=False)
    rlev2 = Column(Float, nullable=False)
    rlev3 = Column(Float, nullable=False)
    rlev4 = Column(Float, nullable=False)
    rlev5 = Column(Float)
    rlev6 = Column(Float)
    rlev7 = Column(Float)
    rlev8 = Column(Float)
    rend = Column(Float, nullable=False)
    sensorpos_id = Column(BigInteger, ForeignKey("sensor_pos.pos_id"))
    sensortype_id = Column(BigInteger, ForeignKey("sensor_type.type_id"))
