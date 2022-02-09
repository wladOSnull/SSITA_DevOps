#!/bin/bash

###
#
# bash script for downloading the project, fixing wrong paths, dependencies, names etc.
# + building with Maven and deploying on Tomcat 9
#
###

### variables
##################################################

G_NAME="Geocit134"
G_REPOSITORY="https://github.com/mentorchita/Geocit134"

G_SERVER_IP="192.168.0.106"
G_DB_IP="192.168.0.102"

G_DB_USERNAME="geocitizen"
G_DB_PASSWORD="weakpass"

G_EMAIL_ADDRESS="???"
G_EMAIL_PASSWORD="???"

### the project
##################################################

### removing
rm -rf $G_NAME

### getting
eval git clone $G_REPOSITORY

### fixing dependencies and packets in 'pom.xml'
##################################################

### 'javax' missing
find ${G_NAME}/ -name "pom.xml" -exec sed -i "s/>servlet-api/>javax.servlet-api/g" {} +

### https for 2 repo
find ${G_NAME}/ -name "pom.xml" -exec sed -i -E "s/(http:\/\/repo.spring)/https:\/\/repo.spring/g" {} +

### redundant nexus repos
find ${G_NAME}/ -name "pom.xml" -exec sed -i "/<distributionManagement>/,/<\/distributionManagement>/d" {} +

### fixing front-end
##################################################

### wrong path to favicon.ico
find ${G_NAME}/src/main/webapp -name "index.html" -exec sed -i 's/\/src\/assets/.\/static/g' {} +

### wrong back-end in minificated .js files
find ./${G_NAME}/src/main/webapp/static/js/ -type f -exec sed -i "s/localhost/${G_SERVER_IP}/g" {} +

### fixing properties of the project deployment
##################################################

sed -i -E \
            "s/(front.url=http:\/\/localhost)/front.url=http:\/\/${G_SERVER_IP}/g; \
            s/(front-end.url=http:\/\/localhost)/front-end.url=http:\/\/${G_SERVER_IP}/g; \

            s/(db.url=jdbc:postgresql:\/\/localhost)/db.url=jdbc:postgresql:\/\/${G_DB_IP}/g;
            s/(db.username=postgres)/db.username=${G_DB_USERNAME}/g;
            s/(db.password=postgres)/db.password=${G_DB_PASSWORD}/g;

            s/(url=jdbc:postgresql:\/\/35.204.28.238)/url=jdbc:postgresql:\/\/${G_DB_IP}/g;
            s/(username=postgres)/username=${G_DB_USERNAME}/g;
            s/(password=postgres)/password=${G_DB_PASSWORD}/g;

            s/(referenceUrl=jdbc:postgresql:\/\/35.204.28.238)/referenceUrl=jdbc:postgresql:\/\/${G_DB_IP}/g;

            s/(email.username=ssgeocitizen@gmail.com)/email.username=${G_EMAIL_ADDRESS}/g;
            s/(email.password=softserve)/email.password=${G_EMAIL_PASSWORD}/g;" ${G_NAME}/src/main/resources/application.properties

### project deploying
##################################################

### reset DB - unstable work of liquibase:dropAll
#(cd Geocit134; eval mvn liquibase:dropAll)

### project building
(cd ${G_NAME}; eval mvn install)

### project deploying
sudo cp ${G_NAME}/target/citizen.war /opt/tomcat/latest/webapps
