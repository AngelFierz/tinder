from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from persistence.base import Base

class Mensajes(Base):
    __tablename__ = 'mensajes'
    id_mensaje = Column(Integer, primary_key=True)
    contenido = Column(String, nullable=False)

    id_remitente = Column(Integer, ForeignKey('perfil.id_perfil'))
    id_destinatario = Column(Integer, ForeignKey('perfil.id_perfil'))

    remitente = relationship("Perfil", back_populates="mensajes_enviados", foreign_keys=[id_remitente])
    destinatario = relationship("Perfil", back_populates="mensajes_recibidos", foreign_keys=[id_destinatario])


