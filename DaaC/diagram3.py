# main
from diagrams import Diagram, Cluster, Edge
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
from diagrams.generic.os import LinuxGeneral
from diagrams.generic.virtualization import Virtualbox

graph_attr = {"splines":"splines",}

# entrypoint
with Diagram("Geocitizen 3",  filename="Geocitizen3", show=False, graph_attr=graph_attr):
    
    with Cluster("VMs", direction="BT"):
    
        with Cluster("DB"):
            centos = Centos()
            psql = Postgresql()
    
            centos >> psql

        with Cluster("Server"):
            geo = Custom("", "./img/geocitizen.png")    
            maven = Custom("", "./img/maven.png")
            tomcat = Custom("", "./img/tomcat.png")
            java = Java()
            ubuntu = Ubuntu()

            ubuntu >> [maven,
                        java,
                        tomcat]

            java - Edge(style="dotted") - \
                    [tomcat,
                    maven,
                    geo]
            
            tomcat >> Edge(style="dashed") >> geo
        
    geo - Edge(style="dotted") - psql
    
    vb = Virtualbox()
    mint = Custom("", "./img/mint.png")

    vb >> Edge(style="dashed") << [ubuntu, centos]
    mint >> Edge(style="dashed") << vb

    
    