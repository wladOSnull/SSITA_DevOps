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
    "fontsize": "40",
    "bgcolor": "transparent",
    "pencolor": "black",
    "penwidth": "4.0",
    "style": "dashed",
    "splines":"spline",
}

# config attribute for AWS cluster
aws_attr = {
    "fontsize": "40",
    "bgcolor": "darkgoldenrod1",
    "splines":"spline",
}

# config attribute for VPC cluster
vpc_attr = {
    "fontsize": "35",
    "bgcolor": "white",
    "splines":"spline",
}

# config attribute for Instance Ubuntu cluster
ubuntu_attr = {
    "fontsize": "30",
    "bgcolor": "#D8F2DEFF",
    "splines":"spline"
}

# config attribute for Instance CentOS cluster
centos_attr = {
    "fontsize": "30", 
    "bgcolor": "#ECE8F6FF",
    "splines":"spline",
}

# config attribute for main cluster
diagram_attr = {
    "fontsize": "50",
    "forcelabels": "true",
    "splines":"spline"
}

# config for all arrows (edges)
main_edge_attr = {
    "minlen": "2.0",
    "penwidth":"5.0",
    "concentrate": "true"
}

### entrypoint
##################################################

with Diagram("Geo Citizen",  filename="Geocitizen3", show=False, graph_attr=diagram_attr, edge_attr=main_edge_attr):

    ### remote infrastructure
    with Cluster("AWS", graph_attr=aws_attr):

        ### group of EC2 instances
        with Cluster("VPC", graph_attr=vpc_attr):

            ### server instance
            with Cluster("Instance Ubuntu", direction="LR", graph_attr=ubuntu_attr):
                
                # variables
                java = Java()
                ubuntu = Ubuntu()
                geo = Custom("", "./img/geocitizen.png")
                tomcat = Custom("", "./img/tomcat.png")
                maven = Custom("", "./img/maven.png")
                ec2_u = EC2()
                
                # links
                java \
                    << Edge(label="usage", style="dashed", fontsize="25") \
                    << maven

                maven >> Edge(label="build", fontsize="25") >> geo

                geo >> Edge(label="usage", style="dashed", fontsize="25") >> java
                tomcat >> Edge(label="host",style="bold", color="darkgreen", fontsize="25") >> geo
                ec2_u - Edge(label="AMI", color="black", style="dotted", fontsize="25") - ubuntu

                ubuntu - Edge(style="dotted") - [tomcat, java, maven, geo]

                # cheat for prettifying
                tomcat >> Edge(color="#00000000") >> java

            ### DB instance
            with Cluster("Instance CentOS", graph_attr=centos_attr):
                
                # variables
                psql = Postgresql()
                centos = Centos()
                ec2_c = EC2()

                # links
                ec2_c - Edge(label="AMI", color="black", style="dotted", fontsize="25") - centos

                centos - Edge(style="dotted") - psql          

    ### inter-groups links
    tomcat >> Edge(color="#00000000") << psql

    geo >> \
        Edge(label="jdbc:connector", style="bold", color="darkgreen", fontsize="25") \
        << psql

### gloabal scope
##################################################

    # variables
    jenkins = Jenkins()
    ansible = Ansible()
    terraform = Terraform()
    
    # global links of IaC
    jenkins \
        << Edge(label="response", style="dotted", color="black", fontsize="25") \
        << terraform

    jenkins \
        >> Edge(label="call 1", style="bold", color="red", fontsize="25") \
        >> terraform

    jenkins \
        >> Edge(label="call 2", style="bold", color="red", fontsize="25") \
        >> ansible \

    terraform \
        >> Edge(label="create", color="black", fontsize="25") \
        >> [ec2_u, ec2_c]

    ansible \
        >> Edge(label="configure", color="black", fontsize="25") \
        >> [tomcat, psql]

    ### human-type links
    User("") >> Edge(label="run", style="bold", color="red", fontsize="25") >> jenkins
    Client("") >> Edge(label="usage", style="bold", color="darkgreen", fontsize="25") << tomcat

### legend
##################################################

    with Cluster(label="Legend", graph_attr=legend_attr):
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
        >> Edge(label="to perform actions with\n creation/configuration/settig up", color="black", fontsize="25") \
        >> none2 \
        >> Edge(label="to use\n / to interact with", color="darkgreen", style="bold", fontsize="25") \
        >> none3 \
        >> Edge(label="to call/trigger for\n performing some actions", color="red", style="bold", fontsize="25") \
        >> none4 \
        >> Edge(label="to response with\n some information/file/etc.", color="black", style="dotted", fontsize="25") \
        >> none5 \
        >> Edge(label="to depend on ...\n / to use smth. to work", color="black", style="dashed", fontsize="25") \
        >> none6

        none6 \
        - Edge(label="to consist\n / to contain", color="black", style="dotted", fontsize="25") \
        - none7