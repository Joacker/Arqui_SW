from clients.Service import Service
from database.session import session
from database.models import Cotizacion, Vendedor, Boleta, Bodega, Producto
import bcrypt, json, os, jwt, datetime
from time import sleep

class Add_product(Service):
    def __init__(self):
        print("Servicio de Añadir Producto")
        super().__init__("bradd")
        self.start_service(debug=True)

    def service_function(self, climsg):
        '''Funcion temporal, sera reemplazada en los distintos servicios'''
        db = session()
        try:
            climsg = json.loads(climsg)
            token = climsg["token"]
            decoded = jwt.decode(
                token, os.environ['SECRET_KEY'], algorithms=['HS256'])
            current_user = db.query(Vendedor).filter_by(id=decoded['id']).first()
            if current_user is None:
                return "Usuario no encontrado"
            valid_cotizacion = db.query(Cotizacion).join(Boleta).filter(current_user.id == Boleta.vendedor_id2).order_by(Cotizacion.id.desc()).first()
            if (valid_cotizacion is None):
                '''No hay cotizaciones creadas'''
                cotizacion = Cotizacion(vendedor_id = current_user.id)
                db.add(cotizacion)
                db.commit()
                cantidadi = climsg["cantidad"]
                nombre_producto1 = climsg["nombre_producto"]
                buscar_prod = db.query(Bodega).filter(Bodega.nombre_producto==nombre_producto1, (Bodega.stock-cantidadi) >= 0).first()
                if(buscar_prod == None):
                    return "No hay stock suficiente, porfavor ingrese otro producto"
                else:
                    '''Se actualiza el stock en función de la cantidad'''
                    #buscar_prod.stock = buscar_prod.stock - cantidadi
                    #db.commit()
                    producto = Producto(bodega_id = buscar_prod.id, cotizacion_id = cotizacion.id, cantidad = cantidadi)
                    db.add(producto)
                    db.commit()
                    print("Agregando boleta")
                    boleta = Boleta( cot_id = cotizacion.id, monto = (buscar_prod.valor_unidad*cantidadi), 
                                    vendedor_id2 = current_user.id, fecha = datetime.datetime.now())
                    db.add(boleta)
                    db.commit()
                return "Cotizacion creada junto con el producto seleccionado"
                    
            else:
                if(valid_cotizacion.concludes == 1):
                    '''No hay cotizaciones creadas'''
                    cotizacion = Cotizacion(vendedor_id = current_user.id)
                    db.add(cotizacion)
                    db.commit()
                    cantidadi = climsg["cantidad"]
                    nombre_producto1 = climsg["nombre_producto"]
                    buscar_prod = db.query(Bodega).filter(Bodega.nombre_producto==nombre_producto1, (Bodega.stock-cantidadi) >= 0).first()
                    if(buscar_prod == None):
                        return "No hay stock suficiente, porfavor ingrese otro producto"
                    else:
                        '''Se actualiza el stock en función de la cantidad'''
                        buscar_prod.stock = buscar_prod.stock - cantidadi
                        db.commit()
                        producto = Producto(bodega_id = buscar_prod.id, cotizacion_id = cotizacion.id, cantidad = cantidadi)
                        db.add(producto)
                        db.commit()
                        print("Agregando boleta")
                        boleta = Boleta( cot_id = cotizacion.id, monto = (buscar_prod.valor_unidad*cantidadi), 
                                        vendedor_id2 = current_user.id, fecha = datetime.datetime.now())
                        db.add(boleta)
                        db.commit()
                    return "Creando nueva cotizacion..."
                else:
                    '''Se busca el producto en la bodega'''
                    cantidadi = climsg["cantidad"]
                    nombre_producto1 = climsg["nombre_producto"]
                    buscar_prod = db.query(Bodega).filter(Bodega.nombre_producto==nombre_producto1, (Bodega.stock-cantidadi) >= 0).first()
                    if(buscar_prod == None):
                        return "No hay stock suficiente, porfavor ingrese otro producto"
                    else:
                        '''Se actualiza el stock en función de la cantidad'''
                        buscar_prod.stock = buscar_prod.stock - cantidadi
                        db.commit()
                        valid_prod_cot = db.query(Producto).filter(Producto.bodega_id == buscar_prod.id, Producto.cotizacion_id == valid_cotizacion.id).first()
                        if (valid_prod_cot is not None):
                            valid_prod_cot.cantidad = valid_prod_cot.cantidad + cantidadi
                            db.commit()
                        else:
                            producto = Producto(bodega_id = buscar_prod.id, cotizacion_id = valid_cotizacion.id, cantidad = cantidadi)
                            db.add(producto)
                            db.commit()
                        boleta = db.query(Boleta).filter(Boleta.cot_id == valid_cotizacion.id).first()
                        boleta.monto = boleta.monto + (buscar_prod.valor_unidad*cantidadi)
                        db.commit()
                    return "Producto añadido a la cotizacion"
        except Exception as e:
            db.close()
            return str(e)
        
        
def main():
    try:
        Add_product()
    except Exception as e:
        print(e)
        sleep(30)
        main()

if __name__ == "__main__":
    main()
