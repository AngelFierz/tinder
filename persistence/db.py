from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

CONNECTION = 'mysql+pymysql://root:admin@localhost/tinderdb'
SessionLocal = sessionmaker(bind = create_engine(CONNECTION, echo = True))