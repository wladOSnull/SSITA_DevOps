# Geocitizen project

**Mint (host) + VBox 6.1.32 Ubuntu (Tomcat 9) + CentOS (PostgreSQL) + java + maven + git + bash + npm**

## Requirements

### Host

Linux Mint 20.3 Una -> [Location: World -	Mirror: LayerOnline](https://mirrors.layeronline.com/linuxmint/stable/20.3/linuxmint-20.3-cinnamon-64bit.iso)
  - Oracle Virtual Box 6.1.32

### DB

CentOS Linux release 7.9.2009 (Core) -> [CentOS-7-x86_64-Minimal-2009.iso](http://mirrors.bytes.ua/centos/7.9.2009/isos/x86_64/)  
- postgres (PostgreSQL) 9.2.24

### Server

Ubuntu 20.04.3 LTS (Focal Fossa) -> [Ubuntu Server 20.04.3 Focal Fossa](https://www.osboxes.org/ubuntu-server/)  
- openjdk 11.0.13 2021-10-19  
- git 2.25.1  
- Apache Tomcat 9.0.58  
- Apache Maven 3.8.4

## Prepare

### VMs creating

- creating VM with Ubuntu 
  - if you need shared folder for Ubuntu -> do 'Appendix-Guest Additions for GUI-less' steps from [*VMs.md*](./VMs.md) 

- to change UIID of .vmi file (due to: cannot register the hard disk with uuid already exists):  
  [stackoverflow](https://stackoverflow.com/questions/44114854/virtualbox-cannot-register-the-hard-disk-already-exists/45391121)

  ```bash
  ~ VBoxManage internalcommands sethduuid <name-of-file>.vdi
  ```

### IP configuring

- reserve IP addresses of all machines on WiFi router (IP addresses in my case)
  - 192.168.0.102 - CentOS (DB)
  - 192.168.0.103 - Mint (host)
  - 192.168.0.106 - Ubuntu (server)

### SSH connection configuring

- installing openssh on Ubuntu

  ```bash
  # installing
  ~ sudo apt install openssh-server

  # starting openssh-server
  ~ sudo systemctl start sshd

  # adding to autostart
  ~ sudo systemctl enable sshd

  # connect to localhost
  ~ ssh localhost
  # type 'yes'

  # disconnect 
  Ctrl+D
  ```

- installing openssh on CentOS 7

  ```bash
  # installing
  ~ sudo yum –y install openssh-server
  
  # starting openssh-server
  ~ sudo systemctl start sshd

  # adding to autostart
  ~ sudo systemctl enable sshd

  # connect to localhost
  ~ ssh localhost
  # type 'yes'

  # disconnect 
  Ctrl+D
  ```

- establish SSH conection to Ubuntu from host

  ```bash
  ~ ssh osboxes@192.168.0.106
  
  # type 'yes'

  # type Ubuntu password of 'osboxes' user

  # disconnect
  Ctrl+D 
  ```

- establish SSH conection to CentOS from host

  ```bash
  ~ ssh centos@192.168.0.102
  
  # type 'yes'

  # type Ubuntu password of 'centos' user

  # disconnect
  Ctrl+D 
  ```

- you can improve accessing to servers with using shortname like `ssh server`

  - [aliases for ssh](https://www.howtogeek.com/75007/stupid-geek-tricks-use-your-ssh-config-file-to-create-aliases-for-hosts/#aoh=16446577456067&referrer=https%3A%2F%2Fwww.google.com&amp_tf=From%20%251%24s&ampshare=https%3A%2F%2Fwww.howtogeek.com%2F75007%2Fstupid-geek-tricks-use-your-ssh-config-file-to-create-aliases-for-hosts%2F)  

---

## Ubuntu - Server

### Presettings 

- installing git 

  ```bash
  # updating apt cache & upgrading system
  ~ sudo apt update && sudo apt upgrade
  
  # installig & checking version of git
  ~ sudo apt install git
  ~ git --version
  ```

- installing Java

  ```bash
  # installig & checking version of git
  ~ sudo apt install openjdk-11-jdk
  ~ java -version

  # checking java folders
  ~ sudo ls -la /usr/lib/jvm/

  # creating symlink for future version managing
  ~ sudo ln -s /usr/lib/jvm/java-1.11.0-openjdk-amd64 /usr/lib/jvm/default-java
  ```

### Apache Tomcat 

- preparing

  - guide -> [Linuxize](https://linuxize.com/post/how-to-install-tomcat-9-on-ubuntu-20-04/)    

  ```bash
  # chrony installing - for right time sync
  ~ sudo apt install chrony 
  ~ sudo systemctl enable chrony

  # adding new user for toomcat
  ~ sudo useradd -m -U -d /opt/tomcat -s /bin/false tomcat

  ~ mkdir Downloads
  ```

- base installing

  ```bash
  # setting of desirable Tomcat version as a variable
  ~ VERSION=9.0.58

  # downloading Tomcat tarball via wget
  ~ wget https://www-eu.apache.org/dist/tomcat/tomcat-9/v${VERSION}/bin/apache-tomcat-${VERSION}.tar.gz -P /tmp

  # unpacknig Tomcat tarball
  ~ sudo tar -xf /tmp/apache-tomcat-${VERSION}.tar.gz -C /opt/tomcat/

  # creating symlink for future version managing
  ~ sudo ln -s /opt/tomcat/apache-tomcat-${VERSION} /opt/tomcat/latest

  # setting up Tomcat's folder as tomcat property
  ~ sudo chown -R tomcat: /opt/tomcat

  # making all Tomcat's scripts executable
  ~ sudo sh -c 'chmod +x /opt/tomcat/latest/bin/*.sh'
  ```
- creating systemd unit for Tomcat

  ```bash
  # adding .service file for managing tomcat via systemctl
  ~ sudo vi /etc/systemd/system/tomcat.service
  ```

  >**! ! !** this setting must be in */etc/systemd system/tomcat.service*:   
  ></br>  
  >[Unit]  
  >Description=Tomcat 9 servlet container  
  >After=network.target
  >
  >[Service]  
  >Type=forking  
  >
  >User=tomcat  
  >Group=tomcat  
  >
  >Environment="JAVA_HOME=/usr/lib/jvm/default-java"  
  >Environment="JAVA_OPTS=-Djava.security.egd=file:///dev/urandom -Djava.awt.headless=true"  
  >
  >Environment="CATALINA_BASE=/opt/tomcat/latest"  
  >Environment="CATALINA_HOME=/opt/tomcat/latest"  
  >Environment="CATALINA_PID=/opt/tomcat/latest/temp/tomcat.pid"  
  >Environment="CATALINA_OPTS=-Xms512M -Xmx1024M -server -XX:+UseParallelGC"  
  >
  >ExecStart=/opt/tomcat/latest/bin/startup.sh  
  >ExecStop=/opt/tomcat/latest/bin/shutdown.sh  
  >
  >[Install]  
  >WantedBy=multi-user.target  

  ```bash
  # informing about/reloading/adding to systemctl new unit
  ~ sudo systemctl daemon-reload

  # adding Tomcat to autostart
  ~ sudo systemctl enable --now tomcat
  # if previous command gets 'Failed to execute operation: Bad message' -> CAREFULLY check tabulation of the .service unit

  # checking status of Tomcat
  ~ sudo systemctl status tomcat
  ```

- *OPTIONAL*: there are command for managing Tomcat's service  

  ```bash
  ~ sudo systemctl start tomcat
  ~ sudo systemctl stop tomcat
  ~ sudo systemctl restart tomcat
  ```

- configuring firewall

  ```bash
  ~ sudo ufw allow 8080/tcp

  # there are more complicate configuration in guide for Tomcat 10
  ```

- visiting of the Tomcat's start page from web browser of host machine

  - on local machine web browser: [ip-of-VM:8080](ip-of-VM:8080)  
  > to get ip of VM: hostname -I

- configuring of tomcat **service users** for accessing "Server Status", "Manager App", "Host Manager" from tomcat start page:  
  
  ```bash
  ~ sudo vi /opt/tomcat/latest/conf/tomcat-users.xml
  ```

  >**! ! !** this setting must be in */opt/tomcat/latest/conf/tomcat-users.xml* before last tag `</tomcat-users>`:  
  >  </br>  
  >`<!-- my settings -->`  
  >`<!-- roles -->`  
  >`<role rolename="admin-gui"/>`  
  >`<role rolename="manager-gui"/>`  
  >`<!-- credentials -->`  
  >`<user username="admin" password="tom" roles="admin-gui"/>`  
  >`<user username="manager" password="jerry" roles="manager-gui"/>`  

  ```bash
  # restarting tomcat.service for applying new tomcat config for users
  ~ sudo systemctl restart tomcat.service
  ~ sudo systemctl status tomcat.service
  ```

### Apache Tomcat - optional coonfiguring

- configuring of accessing to "Server Status", "Manager App" from tomcat start page:

  ```bash
  # add private IP of local machine to "allow="127\.\d+\.\d+\.\d+|::1|0:0:0:0:0:0:0:1" />" string over pipe |
  ~ sudo vi /opt/tomcat/latest/webapps/manager/META-INF/context.xml
  ```

  >**! ! !** this setting must be in */opt/tomcat/latest/webapps/manager/META-INF/context.xml*:  
  >  </br>  
  >allow="127\.\d+\.\d+\.\d+|::1|0:0:0:0:0:0:0:1|192.168.0.103" />

- configuring of accessing to "Host Manager" from tomcat start page:

  ```bash
  # add private IP of local machine to 'allow="127\.\d+\.\d+\.\d+|::1|0:0:0:0:0:0:0:1" />' string with pipe |
  ~ sudo vi /opt/tomcat/latest/webapps/host-manager/META-INF/context.xml
  ```

  >**! ! !** this setting must be in */opt/tomcat/latest/webapps/host-manager/META-INF/context.xml*:  
  >  </br>  
  >allow="127\.\d+\.\d+\.\d+|::1|0:0:0:0:0:0:0:1|192.168.0.103" />

- *OPTIONAL*: changing port of the tomcat server
  
  ```bash
  # change port number on line '<Connector port="8080" protocol="HTTP/1.1"'
  ~ sudo vi /opt/tomcat/conf/server.xml
  ```

  >**! ! !** this setting must be in */opt/tomcat/conf/server.xml*:  
  ></br>  
  ><Connector port="8888" protocol="HTTP/1.1"

  ```bash
  ~ sudo systemctl restart tomcat.service
  ~ sudo systemctl status tomcat.service
  ```

- checking access to "Server Status", "Manager App", "Host Manager" on tomcat start page:
  - click on "Server Status"
    - login: *manager*
    - password: *jerry*
  - click on "Manager App"
    - login: *manager*
    - password: *jerry*
  - click on "Host Manager"
    - login: *admin*
    - password: *tom*

### Maven  

- installing Maven  
  - guide -> [Linuxize](https://linuxize.com/post/how-to-install-apache-maven-on-ubuntu-18-04/)  
  >!!! make symlink with command from THIS .md guide to avoid headache :)  

  ```bash
  ~ cd Downloads
  
  # donwloading Maven via wget
  ~ wget https://dlcdn.apache.org/maven/maven-3/3.8.4/binaries/apache-maven-3.8.4-bin.tar.gz
  ~ sudo tar xf apache-maven-*.tar.gz -C /opt
  ~ ls /opt

  # !!! RIGHT command for creating soft link for better version control
  ~ sudo ln -s ../opt/apache-maven-3.8.4/ /opt/maven

  # symlink HAVE NOT to be RED
  ~ ls -l /opt

  # there must be mvn.sh
  ~ ls /opt/maven/bin
  ```

- configuring Maven environment  
  
  ```bash
  # creating script for loading bunch of variables
  ~ sudo nano /etc/profile.d/maven.sh
  ```

  >**! ! !** this variables must be in */etc/profile.d/maven.sh*:  
    ></br>  
  >export JAVA_HOME=/usr/lib/jvm/default-java  
  >export M2_HOME=/opt/maven  
  >export MAVEN_HOME=/opt/maven  
  >export PATH=\${M2_HOME}/bin:${PATH}  

  ```bash
  # making the script executable
  ~ sudo chmod +x /etc/profile.d/maven.sh

  # loading environment for Maven
  ~ source /etc/profile.d/maven.sh
  ```

- at this point may be needing of logout-login or restarting the VM to applying new environment variables  
  
  ```bash
  # checking Maven version
  ~ mvn -v
  ```

- *OPTIONAL*: adding alias to ~/.bashrc (if 'mvn' command does not work via SSH - ??? an unknown issue)
  
  ```bash
  ~ nano ~/.bashrc
  ```

  >**! ! !** this alias must be in *~/.bashrc*:  
  ></br>  
  >alias mvn='/opt/maven/bin/mvn'  
  
  ```bash
  # loading/applying changes in .bashrc
  ~ . ~/.bashrc  
  ```

---

## CentOS - DB  

### PostgreSQL

- installing PostgreSQL

  ```bash
  # system updating 
  ~ sudo yum update

  # installing PostgreSQL
  ~ sudo yum -y install postgresql-server.x86_64
  # checking version of PostgreSQL
  ~ postgres --version
  ```

- initializing first DB

  ```bash
  # first initialize
  ~ sudo postgresql-setup initdb
  
  # start + enable service unit of  PostgreSQL
  ~ systemctl start postgresql.service
  ~ systemctl enable postgresql.service
  
  # checking status of PostgreSQL
  ~ systemctl status postgresql.service
  ```

- seting up password for super user of PostgreSQL

  ```bash
  # connecting to DB
  ~ sudo -i -u postgres
  ~ psql
  # OR
  ~ sudo -u postgres psql

  # assigning new pass to postgres user
  ~ ALTER USER postgres PASSWORD '<some-pass>';
  
  # logout from PostgreSQL
  ~ \q
  # OR
  Ctrl+D
  ```

  >*TIP*: there is bash script for in the end of this guide for dropping only (if exists) user of DB for the application, creating user of DB for the application, creating DBs for the application and granting privileges on DBs for the user + outputing base info about necessary stuff also **OR** you can make all configuration manually ... :


- creating user for the project and his first own DB

  ```bash
  ~ sudo -U postgres psql

  # creating new user for the project
  ~ CREATE USER geocitizen WITH PASSWORD '<some-pass>';
  ~ ALTER USER geocitizen CREATEDB;

  # list all users
  ~ \du

  # create test DB for new user
  ~ CREATE DATABASE geo_test;
  ~ GRANT ALL PRIVILEGES ON DATABASE geo_test TO geocitizen;

  ~ \q
  ```

- making PostgreSQL databases accessible via login+pass

  ```bash
  # !!! location of pg_hba.conf file may be different
  ~ sudo vi /var/lib/pgsql/data/pg_hba.conf
  ```
  
  >**! ! !** this setting must be in */var/lib/pgsql/data/pg_hba.conf*:  
  ></br>
  > change this one:  
  >|TYPE|DATABASE|USER|ADDRESS|METHOD|
  >|---|---|---|---|---|  
  >|local|all|all|`<empty column>`|peer|
  >
  > to this one:  
  >|TYPE|DATABASE|USER|ADDRESS|METHOD|
  >|---|---|---|---|---|  
  >|local|all|all|`<empty column>`|md5|

  ```bash
  ~ systemctl restart postgresql.service
  ~ systemctl status postgresql.service
  ```

- checking login into DB with username&password of user  

  ```bash
  # psql -d <db-name> -U <user-name>
  ~ psql -d geo_test -U geocitizen
  # input pass of geocitizen user

  # logout
  ~ \q
  ```

- creating DB for the project by user of the project

  ```bash
  ~ psql -d geo_test -U geocitizen
  # type geocitizen's password

  # creating of main DB for the project
  ~ CREATE DATABASE ss_demo_1;

  # creting of test DB for the project
  ~ CREATE DATABASE ss_demo_1_test;

  ~ \q
  ```

- making PostgreSQL accessible from the other machines (Ubuntu as server and Mint as host)
  ```bash
  ~ sudo vi /var/lib/pgsql/data/postgresql.conf
  ```

  >**! ! !** this setting must be in */var/lib/pgsql/data/postgresql.conf*:
  ><br>  
  >`#-------------------------------`  
  >`# CONNECTIONS AND AUTHENTICATION`  
  >`#-------------------------------`  
  >
  >`# - Connection Settings -`  
  >
  >listen_addresses = '*'  
  >port = 5432  

  ```bash
  ~ sudo vi /var/lib/pgsql/data/pg_hba.conf
  ```

  >**! ! !** this setting must be in */var/lib/pgsql/data/pg_hba.conf*:
  ><br>
  >|TYPE|DATABASE|USER|ADDRESS|METHOD|
  >|---|---|---|---|---|    
  >|host|all|all|0.0.0.0/0|md5|  
  >|host|all|all|::/0|md5|

  ```bash
  # check PostgreSQL ports
  ~ ss -l -n |grep 5432
  
  # adding PostgreSQL port to firewall rules
  ~ sudo firewall-cmd --zone=public --add-port=5432/tcp --permanent
  ~ sudo firewall-cmd --reload

  # if firewalld is not running -> systemctl start firewalld
  # if previous command gives an error -> uname -a -> your current kernel must be =^3
  #   if kernel version <3 verssion -> update it
  #   if kernel version =^3 -> just reboot system (that error caused by 'yum update' mainly)
  # after reboot/fixing the problem -> execute foregoing commands

  ~ systemctl restart postgresql.service
  ~ systemctl status postgresql.service
  ```

- at this point you can check connection/accessability to PostgreSQL with installed on Ubuntu or your host machine 'pgAdmin' or 'psql' utility or standart (for Linux) command 'nc' (they are described in Appendix to this guide) 
---

## Ubuntu - The application

### Test building

- building the project
  
  ```bash
  # downloading the project
  ~ cd Downloads  
  ~ git clone https://github.com/mentorchita/Geocit134
  
  # checking files
  ~ cd ~/Downloads/Geocit134/
  ~ ls -l

  # project building
  ~ mvn install
  ```

- at this point we get some errors in project files... fix them

### Fixing

  >*TIP*: there is bash script for in the end of this guide for fixing major of this problems at once (also downloading the project + building by mvn + deploying on Tomcat 9) and it fix the next sites/repositories by replacing 'http' on to 'https' (more likeabe/secure way to fix this POM file) but it fixes only major errors and warnings **OR** you can do all fixing manually ... :

  -----> **Geocit134/pom.xml**

  |fix#|line|problem|fix|type|
  |---|---|---|---|---|
  |1.|173|`<groupId>org.hibernate</groupId>`|`<groupId>org.hibernate.validator</groupId>`|warning|
  |2.|516-522|`<plugin>...</plugin>`|delete this block|warning|
  |3.|494|`<version>3.3.2</version>`|this element is missing, just paste it at 494 line|warning|
  |4.|192|`<artifactId>servlet-api</artifactId>`|`<artifactId>javax.servlet-api</artifactId>`|warning|  
  |5.|~611|`<distributionManagement>...</distributionManagement>`|delete this block|redundant|

  >*IMPORTANT*: for correct work of registration (especially confirming registraion via e-mail) you MUST create new e-mail (gmail, ukr.net etc.) at this point you would have `<name-of-created-email>` and `<pass-for-created-email>`  
  >
  >*IMPORTANT*: if you chose to create a g-mail account DUE TO new Google Terms&Policy you MUST give access for third-party devices/programs in your created g-mail (just search for "Manage third-party apps & services with access to your account" and add this rights for that NEW created account)
  >
  >*IMPORTANT*: DONT use your main account !  


  -----> **Geocit134-exp/src/main/resources/application.properties**

  |fix#|line|problem|fix|type|
  |---|---|---|---|---|
  |1.|2|front.url=http://localhost:8080/citizen/#|front.url=http://192.168.0.106:8080/citizen/#|configuration|  
  |2.|3|front-end.url=http://localhost:8080/citizen/|front-end.url=http://192.168.0.106:8080/citizen/|configuration|
  |3.|6|jdbc:postgresql://localhost:5432/ss_demo_1|jdbc:postgresql://192.168.0.102/ss_demo_1|configuration|  
  |4.|7|db.username=postgres|db.username=geocitizen|configuration|  
  |5.|8|db.password=postgres|db.password=weakpass|configuration|  
  |6.|15|url=jdbc:postgresql://35.204.28.238:5432/ss_demo_1|url=jdbc:postgresql://192.168.0.102:5432/ss_demo_1|configuration|  
  |7.|16|username=postgres|username=geocitizen|configuration|  
  |8.|17|password=postgres|password=weakpass|configuration|  
  |9.|22|referenceUrl=jdbc:postgresql://35.204.28.238:5432/ss_demo_1_test|referenceUrl=jdbc:postgresql://192.168.0.102:5432/ss_demo_1_test|configuration|
  |10.|35|email.username=ssgeocitizen@gmail.com|email.username=`<name-of-created-email>`|configuration|
  |11.|36|email.password=softserve|email.password=`<pass-for-created-email>`|configuration|

- due to error "maven-default-http-blocker (http://0.0.0.0/)" fix the next problem - restricted http repositories  
  - description of the error -> [maven site](https://maven.apache.org/docs/3.8.1/release-notes.html#how-to-fix-when-i-get-a-http-repository-blocked)  

  ```bash
  ~ cd ~/Downloads/Geocit134/
  ~ mkir .mvn

  # unblocking/allowing restricted http repos
  ~ nano .mvn/custom-settings.xml
  ```

  >**! ! !** this seettings must be in *~/Downloads/Geocit134/.mvn/custom-settings.xml*:  
  ></br>   
  >`<settings xmlns="http://maven.apache.org/SETTINGS/1.2.0"
  >          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  >          xsi:schemaLocation="http://maven.apache.org/SETTINGS/1.2.0 http://maven.apache.org/xsd/settings-1.2.0.xsd">`
  >    `<mirrors>`  
  >        `<mirror>`  
  >            `<id>org.springframework.maven.milestone</id>`  
  >            `<mirrorOf>org.springframework.maven.milestone</mirrorOf>`  
  >            `<name>unblocking.org.springframework.maven.milestone</name>`  
  >            `<url>http://repo.spring.io/milestone</url>`  
  >            `<blocked>false</blocked>`  
  >        `</mirror>`
  >
  >	`<mirror>`  
  >            `<id>public</id>`  
  >            `<mirrorOf>public</mirrorOf>`  
  >            `<name>unblocking.public</name>`  
  >            `<url>http://maven.nuxeo.org/nexus/content/groups/public</url>`  
  >            `<blocked>false</blocked>`  
  >        `</mirror>`  
  >
  >	`<mirror>`  
  >            `<id>public-snapshot</id>`  
  >            `<mirrorOf>public-snapshot</mirrorOf>`  
  >            `<name>unblocking.public-snapshot</name>`  
  >            `<url>http://maven.nuxeo.org/nexus/content/groups/public-snapshot</url>`  
  >            `<blocked>false</blocked>`  
  >        `</mirror>`  
  >
  >	`<mirror>`  
  >            `<id>spring-milestone</id>`  
  >            `<mirrorOf>spring-milestone</mirrorOf>`  
  >            `<name>unblocking.spring-milestone</name>`  
  >            `<url>http://repo.spring.io/libs-milestone</url>`  
  >            `<blocked>false</blocked>`  
  >        `</mirror>`  
  >    `</mirrors>`  
  >`</settings>`  

  ```bash
  # binding previous custom settings file and the current project
  ~ nano .mvn/maven.config
  ```

  >**! ! !** this setting must be in *~/Downloads/Geocit134/.mvn/maven.config*:  
  ></br>  
  >--settings .mvn/custom-settings.xml  

### Building

- building the project
  
  ```bash
  ~ cd ~/Downloads/Geocit134/

  # deleting of Maven cache
  ~ rm -rf ~/.m2

  # project building
  ~ mvn install
  ```

### Final

- 'deploying' builded app to Tomcat server

  ```bash
  ~ sudo cp ~Downloads/Geocit134/target/citizen.war /opt/tomcat/latest/webapps/
  ```

- previous step might gives connection error to DB (all main and detailed logs would be written down in /opt/tomcat/latest/logs/catalina.out), so CAREFULLY check logs, inspect ERRORS and fix them :) 

- visiting to the project's application from web browser of host machine

  - on local machine web browser: [ip-of-VM:8080/citizen/#/](ip-of-VM:8080/citizen/#/)  
  - from Tomcat start page: [ip-of-VM:8080](ip-of-VM:8080) -> Manager App -> */citizen*
  > to get ip of VM: hostname -I

---

## Appendix

### Useful commands

- test accessability to PostgreSQL from local  or Ubuntu

  ```bash
  # test access from 
  # local machine
  # Ubuntu server machine
  ~ nc -vz 192.168.0.102 5432

  # test connection with 'psql' (on host machine MUST BE PostgreSQL)
  ~ psql -h 192.168.0.102 -d geo_test -U geocitizen
  # input password of geocitizen user
  ```

- check active connection to PostgreSQL
  
  ```bash
  ~ select * from pg_stat_activity;
  ```
- check logs for Geocitizen app
  
  ```bash
  # main logs of the server/applications/interactions etc.
  ~ sudo less /opt/tomcat/latest/logs/catalina.out
  # also you can press Ctrl+End in 'less' to live mode - Ctrl+C to escape

  # sorting by most recent updated
  ~ sudo ls -lt /opt/tomcat/logs
  
  # reading
  ~ sudo less /opt/tomcat/logs/<most-recent-updated-file>
  ```

- restoring necessary database with Liquibase

  ```bash
  ~ cd ~/Downloads/Geocit134/
  ~ mvn liquibase:update
  # little window will appear to ask permision to appllying queries into DB - click 'Yes'
  ```

- droping DB

  ```bash
  ~ cd ~/Downloads/Geocit134/
  ~ mvn liquibase:dropAll
  # little window will appear to ask permision to cleaning (actually dropping only tables) main DB (ss_demo_1) - click 'Yes'
  ```

### Front-end building  

>*IMPORTANT*: it is NOT RECOMMENDED to build fronted because previous steps or final bash script HAVE TO give you worked project and you would have not reason to build front-end by yourself
>
>*IMPORTANT*: if you decided to build front-end you there is AWARNING - this sources of front-end contain some bugs and you will notice disapearing of 'LOGIN' button on main page and login page would not contain login form as well  

- preparing to build new front-end  
  
  ```bash
  # installing npm (node included into npm)
  ~ sudo apt update
  ~ sudo apt install npm
  
  ~ npm -v
  ~ node -v
  ```

- problem fixing (for succesful building of front-end)

  -----> **Geocit134-exp/front-end/package.json**

  |fix#|line|problem|fix|type|
  |---|---|---|---|---|
  |1.|32|"vue-material": "^1.0.0-beta-7",|just delete "^"|error|

- building new frontend  

  ```bash
  ~ cd ~/Downloads/Geocit134/frond-end/  
  ~ npm install
  ```

- *OPTIONAL*: this command will run front-end + display it's URL
  
  ```bash
  ~ npm run dev
  # previous command print host:port where front-end will be running at that moment
  # visit that host:port from your browser (but check if this port is OPEN for host)

  Ctrl+C

- building

  ```bash
  # building of new front-end - 'dist' folder
  ~ npm run build
  ```

- fixing some bugs after building of front-end

  -----> **Geocit134/front-end/dist/index.html**

  |fix#|line|problem|fix|type|
  |---|---|---|---|---|
  |1.|1|`<link rel="shortcut icon" type=image/ico href=/src/assets/favicon.ico`|`<link rel="shortcut icon" type=image/ico href=./static/favicon.ico>`|404|  
  |2.|1|dot is missing| put dots after `<link href=`|404|  
  |3.|1|dot is missing| put dots after `<script type=text/javascript src=`|404|  

- deploying new front-end

  ```bash
  # copying new front-end to project ('webapp' folder)
  ~ cp -a ~/Downloads/Geocit134/front-end/dist/. ~/Downloads/Geocit134/src/main/webapp
  
  # rebuild the project
  ~ cd ~/Downloads/Geocit134/
  ~ mvn install
  ~ cp target/citizen.war /opt/tomcat/webapp
  ```

- visiting web page
  - on local machine web browser: [ip-of-VM:8080/citizen/#/](ip-of-VM:8080/citizen/#/)  
  - from Tomcat start page: [ip-of-VM:8080](ip-of-VM:8080) -> Manager App -> */citizen*
  >1. to get ip of VM: hostname -I  
  >
  >2. also, 'LOGIN' button would appear only after double click on the map

### Useful links

[aliases for ssh](https://www.howtogeek.com/75007/stupid-geek-tricks-use-your-ssh-config-file-to-create-aliases-for-hosts/#aoh=16446577456067&referrer=https%3A%2F%2Fwww.google.com&amp_tf=From%20%251%24s&ampshare=https%3A%2F%2Fwww.howtogeek.com%2F75007%2Fstupid-geek-tricks-use-your-ssh-config-file-to-create-aliases-for-hosts%2F)  
[installing Nexus on Ubuntu](https://unixcop.com/install-nexus-repository-on-ubuntu-20-04/)  
[installing Tomcat 9 on Ubuntu](https://linuxize.com/post/how-to-install-tomcat-9-on-ubuntu-20-04/)  
[installing node js via npm](https://www.digitalocean.com/community/tutorials/how-to-install-node-js-on-ubuntu-20-04-ru)  

[installing PostgreSQL on Ubuntu](https://www.youtube.com/watch?v=9lq74SafVcw)  
[after installing PostgreSQL on Ubuntu](https://stackoverflow.com/questions/42653690/psql-could-not-connect-to-server-no-such-file-or-directory-5432-error/50882756)  
[after installing PostgreSQL on Ubuntu 2](https://stackoverflow.com/questions/64210167/unable-to-connect-to-postgres-db-due-to-the-authentication-type-10-is-not-suppor) and then
again add password to DB user (to restore pass in MD5 now !)

## Final bash script

### Script for the Geocitizen project's DB (CentOS)

>*IMPORTANT*; this script must be executed on DB machine (CentOS in our case) and it dropping only (if exists) user of DB for the application, creating user of DB for the application, creating DBs for the application and granting privileges on DBs for the user + outputing base info about necessary stuff also.  
>
>*IMPORTANT*: replace all 'variables' for your case (or leave it as well if you configured server, DB, projects properties according to this runbook).  
> 
>*IMPORTANT*: base user of PostgreSQL 'postgres' must be previously setted and 'altered' with password, also there must be accessing to PostgreSQL DBs via md5 (NOT 'peer' method !).

- bash script for:
  - dropping (if exists) user of DB for the application
  - creating user of DB for the application
  - creating DBs for the application
  - granting privileges on DBs for the user
  - checking 
    - user list
    - DB list
    - schemes list on main DB
    - schemes list on test DB

Bash script -> [*db.sh*](./db.sh)

### Script for the Geocitizen project (Ubuntu)

>*IMPORTANT*; this script must be executed on server machine (Ubuntu in our case) and it fixes only major foregoing errors and warnings at once + fixes the problematic sites/repositories by replacing 'http' on to 'https' (actually this is more likeabe/secure way to fix the POM file of this project unlike create permission for mirrors manually) 
>
>*IMPORTANT*: replace `<G_EMAIL_ADDRESS>` and `<G_EMAIL_PASSWORD>` on to credentials of your previously created NEW (NOT THE MAIN) e-mail, also replace all other 'variables'

- bash script for:
  - previously downloading the project  
  - fixing main problems
  - building by mvn  
  - deploying on Tomcat 9

Bash script -> [*project.sh*](./project.sh)
