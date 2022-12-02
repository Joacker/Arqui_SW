COPY bodega(id,stock,nombre_producto,valor_unidad,costo_unidad) 
FROM '/var/lib/postgresql/data/load.csv' 
DELIMITER ';' CSV HEADER;

COPY vendedor(id,rut,nombre,apellido) 
FROM '/var/lib/postgresql/data/vendedores.csv' 
DELIMITER ';' CSV HEADER;