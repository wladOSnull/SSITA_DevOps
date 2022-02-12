### import of modules
##################################################

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

### configurtions for clusters
##################################################

# config attribute for legend cluster
legend_attr = {
    "fontsize": "24",
    "bgcolor": "transparent",
    "pencolor": "black",
    "penwidth": "4.0",
    "style": "dashed",
    "splines":"spline",
}

# config attribute for AWS cluster
aws_attr = {
    "fontsize": "24",
    "bgcolor": "darkgoldenrod1",
    "splines":"spline",
}

# config attribute for VPC cluster
vpc_attr = {
    "fontsize": "22",
    "bgcolor": "white",
    "splines":"spline",
}

# config attribute for Instance Ubuntu cluster
ubuntu_attr = {
    "fontsize": "20",
    "bgcolor": "#D8F2DEFF",
    "splines":"spline",
}

# config attribute for Instance CentOS cluster
centos_attr = {
    "fontsize": "20",
    "bgcolor": "#ECE8F6FF",
    "splines":"spline",
}

# config attribute for instance cluster
diagram_attr = {
    "fontsize": "40",
    "forcelabels": "true",
}

### entrypoint
##################################################

with Diagram("Geocitizen",  filename="Geocitizen1", show=False, graph_attr=diagram_attr):

    ### remote infrastructure
    with Cluster("AWS", graph_attr=aws_attr):

        ### group of EC2 instances
        with Cluster("VPC", graph_attr=vpc_attr):

            ### server instance
            with Cluster("Instance Ubuntu", direction="LR", graph_attr=ubuntu_attr):
                
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
                ec2_u - Edge(label="AMI", color="black", style="dotted") - ubuntu

                ### cheat for prettifying
                tomcat >> Edge(color="#00000000") >> java

            ### DB instance
            with Cluster("Instance CentOS", graph_attr=centos_attr):
                
                # variables
                psql = Postgresql()
                centos = Centos()
                ec2_c = EC2()

                # links
                ec2_c - Edge(label="AMI", color="black", style="dotted") - centos        

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
        >> Edge(label="create", color="black") \
        >> [ec2_u, ec2_c]

    ansible \
        >> Edge(label="configure", color="black") \
        >> [tomcat, psql]

    ### cheat for prettifying
    geo >> Edge(color="#00000000") >> psql
    #geo >> Edge(label="queries", color="darkgreen", style="bold") >> psql

    ### human-type links
    User("DevOps") >> Edge(label="run", style="bold", color="red") >> jenkins
    Client("Clients") >> Edge(label="usage", style="bold", color="darkgreen") >> tomcat

### legend
##################################################

    with Cluster(label="Legend",graph_attr=legend_attr):
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
        >> Edge(label="to perform actions with\n creation/configuration/settig up", color="black") \
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
        - Edge(label="to consist\n / to contain", color="black", style="dotted") \
        - none7