import json
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float,  Boolean, Date
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Bodega(Base):
    __tablename__ = 'bodega'
    id = Column(Integer, primary_key=True)
    stock = Column(Integer, nullable=False)
    nombre_producto = Column(String(90), nullable=False)
    valor_unidad = Column(Integer, nullable=False) #valor de la unidad del producto en la bodega
    costo_unidad = Column(Integer, nullable=False) #valor de la unidad del producto en la tienda
    producto = relationship("Producto", back_populates="bodega")
    def __repr__(self):
        return '<Bodega %r>' % self.bodega_id

class Producto(Base):
    __tablename__ = 'producto'
    cantidad = Column(Integer, nullable=False)
    bodega_id = Column(Integer, ForeignKey('bodega.id'), nullable=False, primary_key=True)
    bodega = relationship('Bodega',back_populates='producto')
    cotizacion_id = Column(Integer, ForeignKey('cotizacion.id'), nullable=False, primary_key=True)
    cotizacion = relationship('Cotizacion', back_populates='producto')
    
    def __repr__(self):
        return '<Producto %r>' % self.cantidad

class Cotizacion(Base):
    __tablename__ = 'cotizacion'
    id = Column(Integer, primary_key=True)
    vendedor_id = Column(Integer, ForeignKey('vendedor.id'), nullable=False)
    concludes = Column(Integer, default=0)
    vendedor = relationship('Vendedor', back_populates='cotizacion')
    boleta = relationship('Boleta', back_populates='cotizacion')
    producto = relationship("Producto", back_populates="cotizacion")
    
    def __repr__(self):
         return '<Cotizacion %r>' % self.cotizacion_id

class Vendedor(Base):
    __tablename__ = 'vendedor'
    id = Column(Integer, primary_key=True)
    rut = Column(String(10), nullable=False)
    password = Column(String(90), nullable=False)
    nombre = Column(String(90), nullable=False)
    apellido = Column(String(90), nullable=False)
    cotizacion = relationship('Cotizacion', back_populates='vendedor')
    boleta = relationship('Boleta', back_populates='vendedor')
    
    def __repr__(self):
         return '<Vendedor %r>' % self.vendedor_id

class Boleta(Base):
    __tablename__ = 'boleta'
    id = Column(Integer, primary_key=True)
    rut = Column(String(10), nullable=True, default=None)
    monto = Column(Integer, nullable=True)
    fecha = Column(DateTime, nullable=True)
    mediopago = Column(String(90), nullable=True)
    vendedor_id2 = Column(Integer, ForeignKey('vendedor.id'), nullable=False)
    vendedor = relationship('Vendedor', back_populates='boleta')
    cot_id = Column(Integer, ForeignKey('cotizacion.id'), nullable=False)
    cotizacion = relationship('Cotizacion', back_populates='boleta')
    medio_pago = relationship('Medio_Pago', back_populates='boleta')
    
    def __repr__(self):
         return '<Boleta %r>' % self.boleta_id

class Medio_Pago(Base):
    __tablename__ = 'medio_pago'
    id = Column(Integer, primary_key=True, autoincrement=True)
    efectivo = Column(Float, default=0)
    debito = Column(Float, default=0)
    credito = Column(Float, default=0)
    boleta_id2 = Column(Integer, ForeignKey('boleta.id'), nullable=False, primary_key=True)
    boleta = relationship('Boleta', back_populates='medio_pago')
    
    def __repr__(self):
         return '<Medio_Pago %r>' % self.medio_pago_id

def to_dict(obj):
    if isinstance(obj.__class__, DeclarativeMeta):
        # an SQLAlchemy class
        fields = {}
        for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
            data = obj.__getattribute__(field)
            try:
                # this will fail on non-encodable values, like other classes
                json.dumps(data)
                if data is not None:
                    fields[field] = data
            except TypeError:
                pass
        # a json-encodable dict
        return fields
