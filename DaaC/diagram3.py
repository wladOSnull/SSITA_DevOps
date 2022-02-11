# main
from diagrams import Diagram, Cluster, Edge, Node
from diagrams.custom import Custom

# DevOps tools
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.iac import Ansible
from diagrams.onprem.iac import Terraform

# base stuff
from diagrams.onprem.compute import Server

# base tools
from diagrams.onprem.database import Postgresql
from diagrams.onprem.vcs import Git
from diagrams.programming.language import Java

# OSs
from diagrams.generic.os import Centos
from diagrams.generic.os import Ubuntu
from diagrams.onprem.client import User
from diagrams.onprem.client import Client

graph_attr = {"splines":"splines",}

# entrypoint
with Diagram("Geocitizen 3",  filename="Geocitizen3", show=False, graph_attr=graph_attr):
    
    with Cluster("EC2", direction="BT"):
    
        with Cluster("Instance - DB"):
            centos = Centos()
            psql = Postgresql()
    
            #centos >> psql

        with Cluster("Instance - Server"):
            geo = Custom("", "./img/geocitizen.png")    
            maven = Custom("", "./img/maven.png")
            tomcat = Custom("", "./img/tomcat.png")
            java = Java()
            ubuntu = Ubuntu()

            maven - Edge(style="dotted") - geo

            java - Edge(style="dotted") - \
                    [tomcat,
                    maven,
                    geo]
            
            tomcat >> Edge(label="host", style="bold") << geo
        
    geo >> Edge(label="queries", color="darkgreen", style="bold") >> psql
    
    #vb = Virtualbox()
    #mint = Custom("", "./img/mint.png")
    jenkins = Jenkins()
    ansible = Ansible()
    terraform = Terraform()

    jenkins >> Edge(label="call 1", color="red", style="bold") >> terraform
    jenkins >> Edge(label="call 2", color="red", style="bold") >> ansible
    ansible >> Edge(label="configure", color="black", style="bold") >> [tomcat, psql]
    terraform >> Edge(label="create", color="black", style="bold") >> [ubuntu, centos]
    terraform >> Edge(label="response", color="black", style="dotted") >> jenkins

    User("DevOps") >> Edge(label="run", style="bold", color="darkgreen") >> jenkins
    Client("Clients") >> Edge(label="usage", style="bold", color="darkgreen") >> geo    
    