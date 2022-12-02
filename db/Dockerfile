FROM postgres:10.5

COPY load.csv .
COPY vendedores.csv .

RUN mv load.csv /var/lib/postgresql/data
RUN mv vendedores.csv /var/lib/postgresql/data

EXPOSE 5432

ENV PGDATA=/var/lib/postgresql/data/some_name/