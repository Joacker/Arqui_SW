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
    bodega = relationship('Bodega', back_populates='producto')
    cotizacion_id = Column(Integer, ForeignKey('cotizacion.id'), nullable=False, primary_key=True)
    cotizacion = relationship('Cotizacion', back_populates='producto')
    
    def __repr__(self):
        return '<Producto %r>' % self.cantidad

class Cotizacion(Base):
    __tablename__ = 'cotizacion'
    id = Column(Integer, primary_key=True)
    vendedor_id = Column(Integer, ForeignKey('vendedor.id'), nullable=False)
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
    rut = Column(String(10), nullable=False)
    nombre = Column(String(90), nullable=False)
    apellido = Column(String(90), nullable=False)
    monto = Column(Integer, nullable=False)
    fecha = Column(DateTime, nullable=False)
    mediopago = Column(String(90), nullable=False)
    vendedor_id2 = Column(Integer, ForeignKey('vendedor.id'), nullable=False)
    vendedor = relationship('Vendedor', back_populates='boleta')
    cot_id = Column(Integer, ForeignKey('cotizacion.id'), nullable=False)
    cotizacion = relationship('Cotizacion', back_populates='boleta')
    medio_pago = relationship('Medio_Pago', back_populates='boleta')
    
    def __repr__(self):
         return '<Boleta %r>' % self.boleta_id

class Medio_Pago(Base):
    __tablename__ = 'medio_pago'
    id = Column(Integer, primary_key=True)
    efectivo = Column(Float, nullable=False)
    debito = Column(Float, nullable=False)
    credito = Column(Float, nullable=False)
    transferencia = Column(Float, nullable=False)
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


'''
class Usuario(Base):
    __tablename__ = 'usuario'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), nullable=True)
    password = Column(String(256), nullable=False)
    email = Column(String(80), nullable=False)
    phone = Column(String(10), nullable=True)
    fecha_ingreso = Column(Date, nullable=True)
    miembro = relationship('Miembro', back_populates='usuario')
    amistad = relationship('Amistad', back_populates='usuario')
    def __repr__(self):
        return '<Usuario %r>' % self.name

class Amistad(Base):
    __tablename__ = 'amistad'
    usuario_id = Column(Integer, ForeignKey('usuario.id'), primary_key=True)
    usuario = relationship('Usuario', back_populates='amistad')
    amigo_id = Column(Integer, nullable=False)

    def __repr__(self):
        return '<Amistad %r>' % self.usuario_id

class Miembro(Base):
    __tablename__ = 'miembro'
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey(
        'usuario.id'), nullable=False)
    usuario = relationship('Usuario', back_populates='miembro')
    rol = Column(String(80), nullable=False)
    admin = Column(Boolean, nullable=False)
    publicaciones = relationship(
        'Publicacion', back_populates='miembro', lazy='dynamic')
    join_date = Column(Date, nullable=True)
    grupo_id = Column(Integer, ForeignKey(
        'grupo.id'), nullable=True)
    grupo = relationship('Grupo', back_populates='miembro')
    def __repr__(self):
        return '<Miembro %r>' % self.usuario_id

class Publicacion(Base):
    __tablename__ = 'publicacion'
    id = Column(Integer, primary_key=True)
    miembro_id = Column(Integer, ForeignKey(
        'miembro.id'), nullable=False)
    miembro = relationship('Miembro', back_populates='publicaciones')
    titulo = Column(String(80), nullable=False)
    descripcion = Column(String(256), nullable=True)
    create_date = Column(Date, nullable=True)
    def __repr__(self):
        return '<Publicacion %r>' % self.contenido

class Grupo(Base):
    __tablename__ = 'grupo'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(80), nullable=False)
    descripcion = Column(String(80), nullable=False)
    miembro = relationship('Miembro', back_populates='grupo', lazy=True)

    def __repr__(self):
        return '<Grupo %r>' % self.name


class Evento(Base):
    __tablename__ = 'evento'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(80), nullable=False)
    descripcion = Column(String(256), nullable=False)
    fecha_inicio = Column(String(256), nullable=False)
    fecha_fin = Column(String(256), nullable=False)
    usuario_id = Column(Integer, ForeignKey(
        'usuario.id'), nullable=False)
    grupo_id = Column(Integer, ForeignKey(
        'grupo.id'), nullable=True)
    def __repr__(self):
        return '<Evento %r>' % self.nombre


class LogoutToken(Base):
    __tablename__ = 'logout_token'
    id = Column(Integer, primary_key=True)
    token = Column(String(256), nullable=False)
    date = Column(DateTime, nullable=False)

    def __repr__(self):
        return '<LogoutToken %r>' % self.token
'''

