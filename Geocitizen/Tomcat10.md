# Tomcat 10

- installing Tomcat 10 by guide  

  -  guide 1 -> [dmosk](https://www.dmosk.ru/miniinstruktions.php?mini=tomcat-install-ubuntu)  
  -  guide 2 -> [andreyex](https://andreyex.ru/ubuntu/kak-ustanovit-tomcat-9-na-ubuntu-20-04/)  

  ```bash
  # system updating
  ~ sudo apt-get update
  ~ sudo hostnamectl set-hostname osboxes.ubuntu.org
  
  # chrony installing - for right time sync
  ~ sudo apt install chrony 
  ~ sudo systemctl enable chrony
  
  # opening of 8080 port for tomcat
  ~ iptables -A INPUT -p tcp --dport 8080 -j ACCEPT 
  ~ sudo iptables -L -v -n | more

  ~ sudo apt install iptables-persistent
  # Yes + Yes
  ~ sudo netfilter-persistent save

  # installing of JAVA
  ~ sudo apt install default-jdk
  ~ java -version

  # adding new user for toomcat
  ~ sudo useradd tomcat -U -s /bin/false -d /opt/tomcat -m
  ~ cat /etc/passwd | grep tomcat

  # swtching to tomcat user
  ~ sudo -u tomcat bash
  ~ whoami
  ~ ctrl+D
  
  # downloading tomcat
  ~ cd Downloads
  ~  wget https://dlcdn.apache.org/tomcat/tomcat-10/v10.0.16/bin/apache-tomcat-10.0.16.tar.gz
  ~ ls -l

  # upacking tomcat into folder of tomcat user /opt/tomcat
  ~ sudo tar zxvf apache-tomcat-*.tar.gz -C /opt/tomcat --strip-components 1
  ~ sudo ls /opt/tomcat
  ~ sudo ls /opt/tomcat/bin/

  # making all shell scripts of tomcat executable
  ~ sudo sh -c 'chmod +x /opt/tomcat/bin/*.sh'
  ~ sudo ls -la /opt/tomcat/bin/

  # running of tomcat
  ~ sudo /opt/tomcat/bin/startup.sh
  ```

- at this point tomcat server must be runned and it works properly, for checking visit:  
  - on tomcat's remote machine/VM: [localhost:8080](localhost:8080)
  - on local machine: [ip-of-VM:8080](ip-of-VM:8080)  
  > to get ip of VM: hostname -I

- setting up autostart of tomcat - part 1  
  
  ```bash
  # shutting down the tomcat server
  ~ sudo /opt/tomcat/bin/shutdown.sh

  # changing owner of all tomcat server's files from root to tomcat user
  ~ ls -l /opt/tomcat
  ~ sudo chown -R tomcat:tomcat /opt/tomcat
  ~ ls -l /opt/tomcat

  # adding .service file for managing tomcat autstart option via systemctl
  ~ sudo vi /etc/systemd/system/tomcat.service
  ```

    >**! ! !** this setting must be in */etc/systemd/system/tomcat.service*:  
    >  </br>
    >[Unit]
    >Description=Apache Tomcat Server
    >After=network.target
    >
    >[Service]
    >Type=forking
    >User=tomcat
    >Group=tomcat
    >Environment="JAVA_HOME=/usr/lib/jvm/default-java"
    >Environment="JAVA_OPTS=-Djava.security.egd=file:///dev/urandom -Djava.awt.headless=true"
    >Environment="CATALINA_BASE=/opt/tomcat"
    >Environment="CATALINA_HOME=/opt/tomcat"
    >Environment="CATALINA_PID=/opt/tomcat/temp/tomcat.pid"
    >Environment="CATALINA_OPTS=-Xms512M -Xmx1024M -server -XX:+UseParallelGC"
    >ExecStart=/opt/tomcat/bin/startup.sh
    >ExecStop=/opt/tomcat/bin/shutdown.sh
    >Restart=on-failure
    >RestartSec=10
    >
    >[Install]
    >WantedBy=multi-user.target

- setting up autostart of tomcat - part 2 final  
  
  ```bash
  # reload systemctl to applying tomcat.service file
  ~ systemctl daemon-reload

  # checking status of tomcat service
  ~ systemctl status tomcat.service

  # running tomcat service
  ~ systemctl start tomcat.service
  ~ systemctl status tomcat.service

  # adding tomcat.service to real autostart
  ~ systemctl enable tomcat.service
  ```

- configuring of tomcat **service users** for accessing "Server Status", "Manager App", "Host Manager" from tomcat start page:  
  
  ```bash
  ~ sudo vi /opt/tomcat/conf/tomcat-users.xml
  ```

  >**! ! !** this setting must be in */opt/tomcat/conf/tomcat-users.xml* before last tag `*</tomcat-users>*`:  
  >  </br>  
  >`<!-- wlados' settings -->`  
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

- *OPTIONAL*: add MAC address of local machine and current/custom private IP to "Address Reservation" in WiFi router settings (private IP address will be static now)

- configuring of accessing to "Server Status", "Manager App" from tomcat start page:

  ```bash
  # add private IP of local machine to 'allow="127\.\d+\.\d+\.\d+|::1|0:0:0:0:0:0:0:1" />' string with pipe |
  ~ sudo vi /opt/tomcat/webapps/manager/META-INF/context.xml
  ```

  >**! ! !** this setting must be in */opt/tomcat/webapps/manager/META-INF/context.xml*:  
  >  </br>  
  >allow="127\.\d+\.\d+\.\d+|::1|0:0:0:0:0:0:0:1|192.168.0.103" />

- configuring of accessing to "Host Manager" from tomcat start page:

  ```bash
  # add private IP of local machine to 'allow="127\.\d+\.\d+\.\d+|::1|0:0:0:0:0:0:0:1" />' string with pipe |
  ~ sudo vi /opt/tomcat/webapps/host-manager/META-INF/context.xml
  ```

  >**! ! !** this setting must be in */opt/tomcat/webapps/host-manager/META-INF/context.xml*:  
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
  ~ systemctl restart tomcat.service
  ~ systemctl status tomcat.service
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