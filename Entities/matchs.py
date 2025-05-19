from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from persistence.base import Base

class Matchs(Base):
    __tablename__ = 'matchs'
    id_match = Column(Integer, primary_key=True)

    id_perfil1 = Column(Integer, ForeignKey('perfil.id_perfil'))
    id_perfil2 = Column(Integer, ForeignKey('perfil.id_perfil'))

    perfil1 = relationship("Perfil", back_populates="matchs1", foreign_keys=[id_perfil1])
    perfil2 = relationship("Perfil", back_populates="matchs2", foreign_keys=[id_perfil2])



