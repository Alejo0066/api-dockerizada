from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

# Tabla de Vehículos
class Vehiculo(Base):
    __tablename__ = "vehiculos"

    id = Column(Integer, primary_key=True, index=True)
    placa = Column(String, unique=True, index=True, nullable=False)
    marca = Column(String, nullable=False)
    modelo = Column(Integer, nullable=False)
    
    # Relación con Reparaciones
    reparaciones = relationship("Reparacion", back_populates="vehiculo")

# Tabla de Reparaciones
class Reparacion(Base):
    __tablename__ = "reparaciones"

    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String, nullable=False)
    costo = Column(Integer, nullable=False)
    vehiculo_id = Column(Integer, ForeignKey("vehiculos.id", ondelete="CASCADE"))

    # Relación con Vehículos
    vehiculo = relationship("Vehiculo", back_populates="reparaciones")
