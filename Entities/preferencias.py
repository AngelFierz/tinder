from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from persistence.base import Base
from Entities.perfil import Perfil

class Preferencias(Base):
    __tablename__ = 'preferencias'
    id_preferencia = Column(Integer, primary_key=True)
    descripcion = Column(String, nullable=False)

    perfiles = relationship("Perfil", back_populates="preferencia")