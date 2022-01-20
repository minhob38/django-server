echo creating initial database

set -e

psql -v ON_ERROR_STOP=1 --username postgres <<-EOSQL
    CREATE DATABASE "docker-database";
EOSQL
