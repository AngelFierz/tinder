from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from persistence.base import Base

class Usuario(Base):
    __tablename__ = 'usuario'
    id_usuario = Column(Integer, primary_key=True)
    nombre_usuario = Column(String, nullable=False)
    correo = Column(String, nullable=False)
    contraseña = Column(String, nullable=False)

    perfil = relationship(
        "Perfil",
        back_populates="usuario",
        uselist=False,
        cascade="all, delete-orphan"
    )


