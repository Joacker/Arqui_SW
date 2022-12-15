from clients.Service import Service
from database.session import session
from database.models import Cotizacion, Vendedor, Boleta, Bodega, Producto, Medio_Pago, to_dict
import json, sys, os, jwt, datetime, time
from time import sleep

class Compra(Service):
    def __init__(self):
        print("Servicio para concretar compra")
        super().__init__("buser")
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
            valid_cotizacion = db.query(Cotizacion).join(Boleta).filter(current_user.id == Boleta.vendedor_id2).first()
            if current_user is None:
                return "Vendedor no encontrado"
            if(valid_cotizacion is None):
                '''No hay cotizaciones creadas'''
                return "No hay cotizaciones creadas, favor crear una"
            elif(valid_cotizacion is not None):
                rut_i = climsg["rut"]
                medio_pago_i = climsg["medio_pago"]
                find_product_to_update =  db.query(Bodega, Producto).join(Producto).filter(Producto.cotizacion_id == valid_cotizacion.id).all()
                cotiid=0
                suma = 0
                for bodega, producto in find_product_to_update:
                    #print(producto.bodega_id, producto.cantidad, bodega.nombre_producto, bodega.valor_unidad)
                    cotiid=producto.cotizacion_id
                    suma = suma + (producto.cantidad * bodega.valor_unidad)
                valid_boleta, cotiza = db.query(Boleta, Cotizacion).join(Cotizacion
                                                                         ).filter(
                                                                             current_user.id == Boleta.vendedor_id2
                                                                        ).filter(
                                                                                Cotizacion.concludes == 0
                                                                            ).first()
                valid_boleta.rut = rut_i
                db.commit()
                
                print(valid_boleta.rut)
                fecha_i = datetime.datetime.now()
                if(cotiza.concludes == 0):
                    if (medio_pago_i == "efectivo"):
                        prodcoti= db.execute("SELECT * FROM producto where cotizacion_id="+str(cotiid)).fetchall()
                        for produni in prodcoti:
                            restar=produni.cantidad
                            buscar=produni.bodega_id
                            afectadas=db.execute("UPDATE bodega SET stock = "+str(restar)+"WHERE id="+str(buscar))
                            #Agregar stock automatico con stock final <5
                            if afectadas:
                                print("Stock ajustado")
                                db.commit()
                            else:
                                print("Error")
                        valid_boleta.rut = rut_i ; db.commit()
                        valid_boleta.mediopago = "efectivo" ; db.commit()
                        valid_boleta.fecha = fecha_i ; db.commit()
                        valid_boleta.monto = suma ; db.commit()
                        medio_pago_concludes_efectivo = Medio_Pago(efectivo = suma, boleta_id2 = valid_boleta.id)
                        db.add(medio_pago_concludes_efectivo)
                        db.commit()
                        cotiza.concludes = 1
                        db.commit()
                        suma = 0
                        return "Compra realizada con efectivo"
                    elif (medio_pago_i == "debito"):
                        prodcoti= db.execute("SELECT * FROM producto where cotizacion_id="+str(cotiid)).fetchall()
                        for produni in prodcoti:
                            restar=produni.cantidad
                            buscar=produni.bodega_id
                            afectadas=db.execute("UPDATE bodega SET stock = "+str(restar)+"WHERE id="+str(buscar))
                            if afectadas:
                                print("Stock ajustado")
                                db.commit()
                            else:
                                print("Error")
                        valid_boleta.rut = rut_i; db.commit()
                        valid_boleta.mediopago = "debito"; db.commit()
                        valid_boleta.fecha = fecha_i ; db.commit()
                        valid_boleta.monto = suma ; db.commit()
                        medio_pago_concludes_debito = Medio_Pago(debito = suma, boleta_id2 = valid_boleta.id)
                        db.add(medio_pago_concludes_debito)
                        db.commit()
                        cotiza.concludes = 1
                        db.commit()
                        suma = 0
                        return "Compra realizada con debito"
                    elif (medio_pago_i == "credito"):
                        prodcoti= db.execute("SELECT * FROM producto where cotizacion_id="+str(cotiid)).fetchall()
                        for produni in prodcoti:
                            restar=produni.cantidad
                            buscar=produni.bodega_id
                            afectadas=db.execute("UPDATE bodega SET stock = "+str(restar)+"WHERE id="+str(buscar))
                            valid_stock = db.query(Bodega).filter(Bodega.id == buscar).first()
                            if (valid_stock.stock < 5):
                                stock_final = valid_stock.stock + 10
                                valid_stock.stock = stock_final
                                print("Stock agregado")
                                db.commit()
                            if afectadas:
                                print("Stock ajustado")
                                db.commit()
                            else:
                                print("Error")
                        valid_boleta.rut = rut_i; db.commit()
                        valid_boleta.mediopago = "credito"; db.commit()
                        valid_boleta.fecha = fecha_i; db.commit()
                        valid_boleta.monto = suma ; db.commit()
                        medio_pago_concludes_credito = Medio_Pago(credito = suma, boleta_id2 = valid_boleta.id)
                        db.add(medio_pago_concludes_credito)
                        db.commit()
                        cotiza.concludes = 1
                        db.commit()
                        suma = 0
                        return "Compra realizada con credito"
                    else:
                        return "Medio de pago no valido"  
                else:
                    return "No hay cotizaciones creadas, favor crear una"
                
        except Exception as e:
            print(e)
            return "Error: " 

def main():
    try:
        Compra()
    except Exception as e:
        print(e)
        sleep(30)
        main()

if __name__ == "__main__":
    main()

