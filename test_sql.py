from models.stargate_networks import StargateNetwork
from data.config import DATABASE_NAME
from models.database import Session

session = Session()

q = session.query(StargateNetwork)
for i in q:
    print(i)