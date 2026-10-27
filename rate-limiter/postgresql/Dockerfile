FROM postgres:18

ENV POSTGRES_DB=school
ENV POSTGRES_USER=admin
ENV POSTGRES_PASSWORD=password

COPY init.sql /docker-entrypoint-initdb.d/init.sql