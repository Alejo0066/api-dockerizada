from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import engine, get_db
from models import Base, Vehiculo, Reparacion
from pydantic import BaseModel

# Crear las tablas en PostgreSQL si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def index():
    return {"message": "FastAPI"}

# ✅ Modelos de Pydantic para validación
class VehiculoCreate(BaseModel):
    placa: str
    marca: str
    modelo: int

class VehiculoUpdate(BaseModel):
    placa: str
    marca: str
    modelo: int

class ReparacionCreate(BaseModel):
    vehiculo_id: int
    descripcion: str
    costo: int

class ReparacionUpdate(BaseModel):
    descripcion: str
    costo: int

# ✅ Endpoint para agregar un vehículo (corregido)
@app.post("/vehiculos/")
def crear_vehiculo(datos: VehiculoCreate, db: Session = Depends(get_db)):
    nuevo_vehiculo = Vehiculo(placa=datos.placa, marca=datos.marca, modelo=datos.modelo)
    db.add(nuevo_vehiculo)
    db.commit()
    db.refresh(nuevo_vehiculo)
    return nuevo_vehiculo

# ✅ Endpoint para obtener todos los vehículos
@app.get("/vehiculos/")
def obtener_vehiculos(db: Session = Depends(get_db)):
    return db.query(Vehiculo).all()

# ✅ Endpoint para obtener un vehículo por ID
@app.get("/vehiculos/{vehiculo_id}")
def obtener_vehiculo(vehiculo_id: int, db: Session = Depends(get_db)):
    vehiculo = db.query(Vehiculo).filter(Vehiculo.id == vehiculo_id).first()
    if not vehiculo:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    return vehiculo

# ✅ Endpoint para actualizar un vehículo
@app.put("/vehiculos/{vehiculo_id}")
def actualizar_vehiculo(vehiculo_id: int, datos: VehiculoUpdate, db: Session = Depends(get_db)):
    vehiculo = db.query(Vehiculo).filter(Vehiculo.id == vehiculo_id).first()
    if not vehiculo:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    
    vehiculo.placa = datos.placa
    vehiculo.marca = datos.marca
    vehiculo.modelo = datos.modelo
    
    db.commit()
    db.refresh(vehiculo)
    return vehiculo

# ✅ Endpoint para eliminar un vehículo
@app.delete("/vehiculos/{vehiculo_id}")
def eliminar_vehiculo(vehiculo_id: int, db: Session = Depends(get_db)):
    vehiculo = db.query(Vehiculo).filter(Vehiculo.id == vehiculo_id).first()
    if not vehiculo:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    
    db.delete(vehiculo)
    db.commit()
    return {"message": "Vehículo eliminado exitosamente"}

# ✅ Endpoint para agregar una reparación a un vehículo (corregido)
@app.post("/reparaciones/")
def crear_reparacion(datos: ReparacionCreate, db: Session = Depends(get_db)):
    vehiculo = db.query(Vehiculo).filter(Vehiculo.id == datos.vehiculo_id).first()
    if not vehiculo:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    
    nueva_reparacion = Reparacion(vehiculo_id=datos.vehiculo_id, descripcion=datos.descripcion, costo=datos.costo)
    db.add(nueva_reparacion)
    db.commit()
    db.refresh(nueva_reparacion)
    return nueva_reparacion

# ✅ Endpoint para obtener todas las reparaciones
@app.get("/reparaciones/")
def obtener_reparaciones(db: Session = Depends(get_db)):
    return db.query(Reparacion).all()

# ✅ Endpoint para obtener una reparación por ID
@app.get("/reparaciones/{reparacion_id}")
def obtener_reparacion(reparacion_id: int, db: Session = Depends(get_db)):
    reparacion = db.query(Reparacion).filter(Reparacion.id == reparacion_id).first()
    if not reparacion:
        raise HTTPException(status_code=404, detail="Reparación no encontrada")
    return reparacion

# ✅ Endpoint para actualizar una reparación
@app.put("/reparaciones/{reparacion_id}")
def actualizar_reparacion(reparacion_id: int, datos: ReparacionUpdate, db: Session = Depends(get_db)):
    reparacion = db.query(Reparacion).filter(Reparacion.id == reparacion_id).first()
    if not reparacion:
        raise HTTPException(status_code=404, detail="Reparación no encontrada")
    
    reparacion.descripcion = datos.descripcion
    reparacion.costo = datos.costo
    
    db.commit()
    db.refresh(reparacion)
    return reparacion

# ✅ Endpoint para eliminar una reparación
@app.delete("/reparaciones/{reparacion_id}")
def eliminar_reparacion(reparacion_id: int, db: Session = Depends(get_db)):
    reparacion = db.query(Reparacion).filter(Reparacion.id == reparacion_id).first()
    if not reparacion:
        raise HTTPException(status_code=404, detail="Reparación no encontrada")
    
    db.delete(reparacion)
    db.commit()
    return {"message": "Reparación eliminada exitosamente"}




