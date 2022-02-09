#!/bin/bash

###
#
# bash script for dropping (if exists) user, privileges, DBs 
# + creating DB user, DB user's pass, DBs, privileges
# + output base info about necessary stuff
#
###

### variables
##################################################

DB_SUPER_USER='postgres'
DB_SUPER_PASS='???'

DB_GEO_USER='geocitizen'
DB_GEO_PASS='weakpass'

DB_MAIN_NAME='ss_demo_1'
DB_TEST_NAME='ss_demo_1_test'

### configuration
##################################################

### dropping (if exists) user of DB for the application
### creating user of DB for the application
### creating DBs for the application
### granting privileges on DBs for the user 
PGPASSWORD=${DB_SUPER_PASS} psql -U ${DB_SUPER_USER} \
<< EOF
    DROP DATABASE IF EXISTS ${DB_MAIN_NAME};
    DROP DATABASE IF EXISTS ${DB_TEST_NAME};
    DROP OWNED BY ${DB_GEO_USER};
    DROP USER IF EXISTS ${DB_GEO_USER};
    
    CREATE USER ${DB_GEO_USER} WITH PASSWORD '${DB_GEO_PASS}';
    ALTER USER ${DB_GEO_USER} CREATEDB;
    
    CREATE DATABASE ${DB_MAIN_NAME};
    CREATE DATABASE ${DB_TEST_NAME};
    GRANT ALL PRIVILEGES ON DATABASE ${DB_MAIN_NAME}, ${DB_TEST_NAME} TO ${DB_GEO_USER};
EOF

### checking
##################################################

### user list
### DB list
### switch to main DB & schemes list on main DB
### switch to test DB & schemes list on test DB
PGPASSWORD=${DB_GEO_PASS} psql -d ${DB_MAIN_NAME} -U ${DB_GEO_USER} \
<< EOF
    \du
    \l

    \c ${DB_MAIN_NAME}
    \d

    \c ${DB_TEST_NAME}
    \d
EOF
