# main
from diagrams import Diagram, Cluster, Edge
from diagrams.custom import Custom

# DevOps tools
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.iac import Ansible
from diagrams.onprem.iac import Terraform

# base technologies
from diagrams.onprem.compute import Server
from diagrams.generic.virtualization import Virtualbox

# OSs
from diagrams.generic.os import Centos
from diagrams.generic.os import Ubuntu
from diagrams.generic.os import LinuxGeneral

# base tools
from diagrams.programming.language import Java
from diagrams.onprem.database import Postgresql
from diagrams.onprem.vcs import Git
from diagrams.onprem.vcs import Github

# entrypoint
with Diagram("Geocitizen 1",  filename="Geocitizen1", show=False):

    jenkins = Jenkins()
    github = Github("Geocit134")
    ansible = Ansible()
    terraform = Terraform()

   # with Cluster("Remote Servers"):
        
        
    with Cluster("Ubuntu", direction="LR") as wer:
        java = Java()
        ubuntu = Ubuntu()
        tomcat = Custom("", "./img/tomcat.png")
        maven = Custom("", "./img/maven.png")

        tomcat \
        >> Edge(color="firebrick", style="dashed") \
        << java
        maven \
        >> Edge(color="firebrick", style="dashed") \
        << java

    with Cluster("CentOS"):
        psql = Postgresql()
        centos = Centos()

    tomcat - \
        Edge(label="jdbc:connector") \
        - psql


    jenkins \
        >> Edge(label="call 1", style="bold", color="black") \
        >> terraform

    terraform \
        >> Edge(label="response", style="bold", color="black") \
        >> jenkins

    jenkins \
        >> Edge(label="call 2", style="bold", color="black") \
        >> ansible \
        >> Edge(label="get project", style="dashed") \
        << github

    terraform \
        >> Edge(label="create") \
        >> [centos, ubuntu]


    ansible \
        >> Edge(label="configure") \
        >> tomcat

    ansible \
        >> Edge(label="configure") \
        >> psql