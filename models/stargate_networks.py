from sqlalchemy import Column, Integer, String, ForeignKey

from models.database import Base


class StargateNetwork(Base):
    __tablename__ = 'stargate network'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    endpointId = Column(Integer)
    poolNative = Column(String)

    def __init__(self, name: str, endpointId: int, poolNative: str):
        self.name = name
        self.endpointId = endpointId
        self.poolNative = poolNative

    def __repr__(self):
        info: str = f'Имя сети = {self.name} endpointId = {self.endpointId}'
        return info
