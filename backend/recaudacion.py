from clients.Service import Service
from database.session import session
from database.models import Vendedor, Bodega, Boleta
import json, sys, os, datetime
from time import sleep

class Catalogo(Service):
    def __init__(self):
        print("Informe sobre Recaudación")
        super().__init__("breca")
        self.start_service(debug=True)

    def service_function(self, climsg):
        '''Funcion temporal, sera reemplazada en los distintos servicios'''
        db = session()
        try:
            climsg = json.loads(climsg)
            choice = climsg["choice"]
            if (choice == "1"): 
                recaudacion = db.query(Boleta).filter().all()
                recaudacion=db.execute("SELECT SUM(monto) as total ,mediopago FROM boleta group by mediopago order by total asc").fetchall()
                #recaudacion = db.query(Boleta).filter().all()
                print("Total Recaudado:")
                list_products = ""
                lista=list()
                index = 0
                for c in recaudacion:
                    
                    if c.mediopago is None:
                        #print(c.total,"No especificado")
                        if (index == (len(recaudacion)-1)):
                            list_products = list_products + "#Total: "+str(c.total)+" ;; Medio de Pago: No especificado"
                        else:
                            list_products = list_products + "#Total: "+str(c.total)+" ;; Medio de Pago: No especificado"+","
                        
                            
                    else:
                        #print(c.total,c.mediopago)
                        if (index == (len(recaudacion)-1)):
                            list_products = list_products + "#Total: "+str(c.total)+" ;; Medio de Pago: "+str(c.mediopago)
                        else:
                            list_products = list_products + "#Total: "+str(c.total)+" ;; Medio de Pago: "+str(c.mediopago)+","
                        



                    
                    
                    index = index + 1
                index = 0
                return list_products
            elif (choice == "2"):
                fecha1 = climsg["fecha1"]
                fecha2 = climsg["fecha2"]
                recaudacion=db.execute("SELECT SUM(monto) as total ,mediopago FROM boleta  where fecha between '"+fecha1+"' and '"+fecha2+"' group by mediopago order by total asc").fetchall()
                print("Total Recaudado:")
                list_products = ""
                lista=list()
                index = 0
                for c in recaudacion:
                    
                    if c.mediopago is None:
                        #print(c.total,"No especificado")
                        if (index == (len(recaudacion)-1)):
                            list_products = list_products + "#Total: "+str(c.total)+" ;; Medio de Pago: No especificado"
                        else:
                            list_products = list_products + "#Total: "+str(c.total)+" ;; Medio de Pago: No especificado"+","
                        
                            
                    else:
                        #print(c.total,c.mediopago)
                        if (index == (len(recaudacion)-1)):
                            list_products = list_products + "#Total: "+str(c.total)+" ;; Medio de Pago: "+str(c.mediopago)
                        else:
                            list_products = list_products + "#Total: "+str(c.total)+" ;; Medio de Pago: "+str(c.mediopago)+","
                    index = index + 1
                index = 0
                return list_products
            elif (choice == "3"):
                Rut = climsg["rut"]
                recaudacion=db.execute("SELECT SUM(monto) as total ,mediopago FROM boleta,vendedor  where Vendedor.rut='"+Rut+"' and boleta.vendedor_id2=Vendedor.id group by mediopago order by total asc").fetchall()
                list_products = ""
                lista=list()
                index = 0
                for c in recaudacion:
                    
                    if c.mediopago is None:
                        #print(c.total,"No especificado")
                        if (index == (len(recaudacion)-1)):
                            list_products = list_products + "#Total: "+str(c.total)+" ;; Medio de Pago: No especificado"
                        else:
                            list_products = list_products + "#Total: "+str(c.total)+" ;; Medio de Pago: No especificado"+","
                        
                            
                    else:
                        #print(c.total,c.mediopago)
                        if (index == (len(recaudacion)-1)):
                            list_products = list_products + "#Total: "+str(c.total)+" ;; Medio de Pago: "+str(c.mediopago)
                        else:
                            list_products = list_products + "#Total: "+str(c.total)+" ;; Medio de Pago: "+str(c.mediopago)+","
                    index = index + 1
                index = 0
                return list_products
                

            

            
            elif (choice == "4"):
                return "Cerrando catalogo de productos"
                
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            return "Error: " + str(e) + " " + fname + " " + str(exc_tb.tb_lineno)


def main():
    try:
        Catalogo()
    except Exception as e:
        print(e)
        sleep(30)
        main()

if __name__ == "__main__":
    main()
