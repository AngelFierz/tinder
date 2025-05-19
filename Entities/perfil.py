from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from persistence.base import Base
from Entities.matchs import Matchs
from Entities.mensajes import Mensajes

class Perfil(Base):
    __tablename__ = 'perfil'
    id_perfil = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    genero = Column(String, nullable=False)
    descripcion = Column(String, nullable=False)
    hijos = Column(Integer)

    id_usuario = Column(Integer, ForeignKey('usuario.id_usuario'), unique=True)
    usuario = relationship("Usuario", back_populates="perfil", uselist=False)

    id_preferencia = Column(Integer, ForeignKey('preferencias.id_preferencia'))
    preferencia = relationship("Preferencias", back_populates="perfiles")

    matchs1 = relationship("Matchs", back_populates="perfil1", foreign_keys=[Matchs.id_perfil1], cascade="all, delete-orphan")
    matchs2 = relationship("Matchs", back_populates="perfil2", foreign_keys=[Matchs.id_perfil2], cascade="all, delete-orphan")
    mensajes_enviados = relationship("Mensajes", back_populates="remitente", foreign_keys=[Mensajes.id_remitente], cascade="all, delete-orphan")
    mensajes_recibidos = relationship("Mensajes", back_populates="destinatario", foreign_keys=[Mensajes.id_destinatario], cascade="all, delete-orphan")


