from sqlalchemy import Column, Integer, String
from persistence.base import Base

class Usuario(Base):
    __tablename__ = 'usuario'
    id_usuario = Column(Integer, primary_key = True)
    nombre_usuario = Column(String)
    correo = Column(String)
    contraseña = Column(String)