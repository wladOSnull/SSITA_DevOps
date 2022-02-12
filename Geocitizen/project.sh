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
echo -e "##################################################\nRemoving the old project\n##################################################\n"
rm -rf $G_NAME

### getting
echo -e "##################################################\nClonning the project again\n##################################################\n"
git clone $G_REPOSITORY

### fixing dependencies and packets in 'pom.xml'
##################################################

echo -e "\n##################################################\nThe small error the old project\n##################################################\n"

### 'javax' missing
find ${G_NAME}/ -name "pom.xml" -exec sed -i "s/>servlet-api/>javax.servlet-api/g" {} +

### https for 2 repo
find ${G_NAME}/ -name "pom.xml" -exec sed -i -E "s/(http:\/\/repo.spring)/https:\/\/repo.spring/g" {} +

### redundant nexus repos
find ${G_NAME}/ -name "pom.xml" -exec sed -i "/<distributionManagement>/,/<\/distributionManagement>/d" {} +

### missing version of maven war plugin
printf '%s\n' '0?<artifactId>maven-war-plugin<\/artifactId>?a' '<version>3.3.2</version>' . x | ex ${G_NAME}/"pom.xml"

### missing 'validator' attribute
sed -i -E ':a;N;$!ba; s/org.hibernate/org.hibernate.validator/2' ${G_NAME}/"pom.xml"

### remove duplicates
##################################################

echo -e "##################################################\nRemoving duplicates\n##################################################\n"

### function for deleting xml block with specified string
function REMOVE_XML()
{
    ### $1 - UP TO
    ### $2 - DOWN TO
    echo -e "${1} ---------- ${2}\n"

    ### delete duplicate TOP
    EDGE=true
    while [ "$EDGE" = true ]; do
        
        if ! [[ "$DUPLICATE_LINE" == "${1}" ]]; then
            sed -i "${DUPLICATE_NUMBER}d" ${G_NAME}/pom.xml
        
            ((DUPLICATE_NUMBER--))
        else
            EDGE=false
            ((DUPLICATE_NUMBER+=1))    
        fi
        
        DUPLICATE_LINE=`sed -n "${DUPLICATE_NUMBER}p" < ${G_NAME}/pom.xml`
        DUPLICATE_LINE=`echo $DUPLICATE_LINE | sed 's/ *$//g'`
    done

    ### delete duplicate DOWN
    EDGE=true
    while [ "$EDGE" = true ]; do
        
        if ! [[ "$DUPLICATE_LINE" == "${2}" ]]; then
            sed -i "${DUPLICATE_NUMBER}d" ${G_NAME}/pom.xml

            DUPLICATE_LINE=`sed -n "${DUPLICATE_NUMBER}p" < ${G_NAME}/pom.xml`
            DUPLICATE_LINE=`echo $DUPLICATE_LINE | sed 's/ *$//g'`
        else
            EDGE=false
        fi
    done
}

### get the duplicate of maven war plugin
DUPLICATE_NUMBER=`grep -n -m1 'maven-war' ${G_NAME}/pom.xml | cut -f1 -d:`
DUPLICATE_LINE=`sed -n "${DUPLICATE_NUMBER}p" < ${G_NAME}/pom.xml`
DUPLICATE_LINE=`echo $DUPLICATE_LINE | sed 's/ *$//g'`
TOP="<plugins>"
DOWN="<plugin>"

### remove it
REMOVE_XML $TOP $DOWN

### get the duplicate of postgresql plugin
DUPLICATE_NUMBER=`grep -n "org.postgresql" ${G_NAME}/pom.xml | sed -n 2p | cut -f1 -d:`
DUPLICATE_LINE=`sed -n "${DUPLICATE_NUMBER}p" < ${G_NAME}/pom.xml`
DUPLICATE_LINE=`echo $DUPLICATE_LINE | sed 's/ *$//g'`
TOP="</dependency>"
DOWN="<!--Servlet API-->"

### remove it
REMOVE_XML $TOP "${DOWN}"

### fixing front-end
##################################################

echo -e "##################################################\nFront-end fixing\n##################################################\n"

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

echo -e "##################################################\nThe project building\n##################################################\n"

### reset DB - unstable work of liquibase:dropAll
#(cd Geocit134; eval mvn liquibase:dropAll)

### project building
#(cd ${G_NAME}; eval mvn install)

echo -e "\n##################################################\nThe project deploying\n##################################################\n"

### project deploying
#sudo cp ${G_NAME}/target/citizen.war /opt/tomcat/latest/webapps