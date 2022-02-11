# main
from diagrams import Diagram, Cluster, Edge
from diagrams.custom import Custom

# DevOps tools
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.iac import Ansible
from diagrams.onprem.iac import Terraform

# OSs
from diagrams.aws.compute import EC2
from diagrams.generic.os import Centos
from diagrams.generic.os import Ubuntu

# base tools
from diagrams.programming.language import Java
from diagrams.onprem.database import Postgresql
from diagrams.onprem.client import User
from diagrams.onprem.client import Client

# entrypoint
with Diagram("Geocitizen",  filename="Geocitizen1", show=False):

    jenkins = Jenkins()
    ansible = Ansible()
    terraform = Terraform()

    with Cluster("AWS"):
        with Cluster("VPC"):
            with Cluster("Instance Ubuntu", direction="LR") as wer:
                java = Java()
                ubuntu = Ubuntu()
                geo = Custom("Geocit134", "./img/geocitizen.png")
                tomcat = Custom("", "./img/tomcat.png")
                maven = Custom("", "./img/maven.png")
                ec2_u = EC2()
                
                java \
                    << Edge(label="usage", style="dashed") \
                    << maven

                maven >> Edge(label="build") >> geo

                #tomcat >> Edge(label="usage", style="dashed") >> java
                tomcat >> Edge(color="#00000000") >> java
                tomcat >> Edge(label="host",style="bold", color="darkgreen") >> geo

                ec2_u - Edge(label="AMI", style="dotted") - ubuntu

            with Cluster("Instance CentOS", direction="BT"):
                psql = Postgresql()
                centos = Centos()
                ec2_c = EC2()
                ec2_c - Edge(label="AMI", style="dotted") - centos
                

    jenkins \
        << Edge(label="response", style="dotted", color="black") \
        << terraform

    tomcat >> \
        Edge(label="jdbc:connector", style="bold", color="darkgreen") \
        << psql

    jenkins \
        >> Edge(label="call 1", style="bold", color="red") \
        >> terraform

    jenkins \
        >> Edge(label="call 2", style="bold", color="red") \
        >> ansible \

    terraform \
        >> Edge(label="create") \
        >> [ec2_u, ec2_c]
        #>> [centos, ubuntu]

    ansible \
        >> Edge(label="configure") \
        >> [tomcat, psql]

    geo >> Edge(color="#00000000", style="bold") >> psql
    #geo >> Edge(label="queries", color="darkgreen", style="bold") >> psql

    User("DevOps") >> Edge(label="run", style="bold", color="darkgreen") >> jenkins
    Client("Clients") >> Edge(label="usage", style="bold", color="darkgreen") >> tomcat

    Edge(label="type1", color="darkgreen")