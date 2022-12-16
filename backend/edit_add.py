from clients.Service import Service
from database.session import session
from database.models import Vendedor, Bodega
from sqlalchemy import insert
import json, sys, os, datetime
from time import sleep

class Edit_add(Service):
    def __init__(self):
        print("Servicio de Editar o Agregar productos en la bodega")
        super().__init__("bedit")
        self.start_service(debug=True)
        
    def service_function(self, climsg):
        db = session()
        try:
            climsg = json.loads(climsg)
            choice = climsg["choice"]
            if (choice == "1"):
                print("editando producto de la bodega")
                choice2 = climsg["choice2"]
                ID = climsg["ID"]
                print(ID)
                
                if(choice2 == "1"):
                    producto_edit = db.query(Bodega).filter(Bodega.id == ID ).first()
                    stock_edit = climsg["stock"]
                    #prod = Bodega(stock=stock_edit ,nombre_producto= producto_edit.nombre_producto , valor_unidad= producto_edit.valor_unidad, costo_unidad=producto_edit.costo_unidad)
                    #db.delete(Bodega).filter(Bodega.id == ID ).all()
                    producto_edit.stock = stock_edit
                    db.commit()
                    #Bodega.stock = stock_edit
                    print(stock_edit)
                    return "PRODUCTO EDITADO CON RESPECTO AL stock"
                elif(choice2 == "2"):
                    producto_edit2 = db.query(Bodega).filter(Bodega.id == ID ).first()
                    valor_unidad_edit = climsg["valor_unidad"]
                    producto_edit2.valor_unidad = valor_unidad_edit
                    db.commit()
                    #Bodega.valor_unidad = valor_unidad_edit
                    print(valor_unidad_edit)
                    return "PRODUCTO EDITADO CON RESPECTO AL valor_unidad"
                
                return "PRODUCTO EDITADO"
            elif (choice == "2"):
                stock_input  = climsg["stock"]
                nombre_producto_input  = climsg["nombre_producto"]
                valor_unidad_input = climsg["valor_unidad"]
                costo_unidad_input= climsg["costo_unidad"]
                print("agregando producto en la bodega")
                print(stock_input )
                print(nombre_producto_input )
                print(valor_unidad_input )
                print(costo_unidad_input )
                a = db.query(Bodega).filter(Bodega.stock > 0).all()
                aux = len(a)
                print("los id son ",len(a))
                producto = Bodega(stock=stock_input ,nombre_producto= nombre_producto_input , valor_unidad= valor_unidad_input , costo_unidad=costo_unidad_input)
                db.add(producto)
                db.commit()
                #aux = db.add(Bodega).

                return "AGREGADO EN BODEGA"
                
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            return "Error: " + str(e) + " " + fname + " " + str(exc_tb.tb_lineno)
        
        
def main():
    try:
        Edit_add()
    except Exception as e:
        print(e)
        sleep(30)
        main()

if __name__ == "__main__":
    main()