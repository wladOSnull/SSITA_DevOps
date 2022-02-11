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

### entrypoint
##################################################

with Diagram("Geocitizen",  filename="Geocitizen1", show=False):

    ### remote infrastructure
    with Cluster("AWS"):

        ### group of EC2 instances
        with Cluster("VPC"):

            ### server instance
            with Cluster("Instance Ubuntu", direction="LR") as wer:
                
                # variables
                java = Java()
                ubuntu = Ubuntu()
                geo = Custom("Geocit134", "./img/geocitizen.png")
                tomcat = Custom("", "./img/tomcat.png")
                maven = Custom("", "./img/maven.png")
                ec2_u = EC2()
                
                # links
                java \
                    << Edge(label="usage", style="dashed") \
                    << maven

                maven >> Edge(label="build") >> geo

                #tomcat >> Edge(label="usage", style="dashed") >> java
                tomcat >> Edge(label="host",style="bold", color="darkgreen") >> geo
                ec2_u - Edge(label="AMI", style="dotted") - ubuntu

                ### cheat for prettifying
                tomcat >> Edge(color="#00000000") >> java

            ### DB instance
            with Cluster("Instance CentOS", direction="BT"):
                
                # variables
                psql = Postgresql()
                centos = Centos()
                ec2_c = EC2()

                # links
                ec2_c - Edge(label="AMI", style="dotted") - centos          

    # inter-groups links
    tomcat >> \
        Edge(label="jdbc:connector", style="bold", color="darkgreen") \
        << psql

### gloabal scope
##################################################

    # variables
    jenkins = Jenkins()
    ansible = Ansible()
    terraform = Terraform()
    
    # global links of IaC
    jenkins \
        << Edge(label="response", style="dotted", color="black") \
        << terraform

    jenkins \
        >> Edge(label="call 1", style="bold", color="red") \
        >> terraform

    jenkins \
        >> Edge(label="call 2", style="bold", color="red") \
        >> ansible \

    terraform \
        >> Edge(label="create") \
        >> [ec2_u, ec2_c]

    ansible \
        >> Edge(label="configure") \
        >> [tomcat, psql]

    ### cheat for prettifying
    geo >> Edge(color="#00000000") >> psql
    #geo >> Edge(label="queries", color="darkgreen", style="bold") >> psql

    ### human-type links
    User("DevOps") >> Edge(label="run", style="bold", color="red") >> jenkins
    Client("Clients") >> Edge(label="usage", style="bold", color="darkgreen") >> tomcat

### legend
##################################################

    # empty variables
    none1 = Custom("", "./img/null.png")
    none2 = Custom("", "./img/null.png")
    none3 = Custom("", "./img/null.png")
    none4 = Custom("", "./img/null.png")
    none5 = Custom("", "./img/null.png")
    none6 = Custom("", "./img/null.png")
    none7 = Custom("", "./img/null.png")
    
    # descri[tion for all types of arrows
    none1 \
    >> Edge(label="to perform actions with\n creation/configuration/settig up") \
    >> none2 \
    >> Edge(label="to use\n / to interact with", color="darkgreen", style="bold") \
    >> none3 \
    >> Edge(label="to call/trigger for\n performing some actions", color="red", style="bold") \
    >> none4 \
    >> Edge(label="to response with\n some information/file/etc.", color="black", style="dotted") \
    >> none5 \
    >> Edge(label="to depend on ...\n / to use smth. to work", color="black", style="dashed") \
    >> none6

    none6 \
    - Edge(label="to consist\n / to contain", style="dotted") \
    - none7