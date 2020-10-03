#!/bin/sh
[ -f ./.env ] && source ./.env || { echo ".env does not exist!" && exit 1; }

# create a role with a user, use permission inheritance for convenience
echo "Setting up database roles"
PGPASSWORD="${POSTGRES_PASSWORD}" psql ${SELECT_DATABASE} -p ${DBPORT} -U ${POSTGRES_USER} postgres <<SQL
create role ${DBROLE} createdb;
create user ${DBUSER} createrole inherit password '${DBPASS}';
grant ${DBROLE} to ${DBUSER};
alter role ${DBROLE} set client_encoding to 'utf8';
alter role ${DBROLE} set default_transaction_isolation to 'read committed';
alter role ${DBROLE} set timezone to 'UTC';
SQL

# create the database(es)
echo "Creating database: ${DBNAME}"
PGPASSWORD="${POSTGRES_PASSWORD}" psql ${SELECT_DATABASE} -p ${DBPORT} -U ${POSTGRES_USER} postgres <<SQL
drop database ${DBNAME};
create database ${DBNAME} with owner ${DBROLE};
grant all privileges on database ${DBNAME} to ${DBROLE};
SQL

