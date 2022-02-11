# main
from diagrams import Diagram, Cluster, Edge
from diagrams.custom import Custom

# DevOps tools
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.iac import Ansible
from diagrams.onprem.iac import Terraform

# base stuff
from diagrams.onprem.compute import Server
from diagrams.aws.compute import EC2

# base tools
from diagrams.onprem.database import Postgresql
from diagrams.onprem.vcs import Github

# entrypoint
with Diagram("Geocitizen 2",  filename="Geocitizen2", show=False):

    jenkins = Jenkins()
    ansible = Ansible()
    terraform = Terraform()
    github = Github("Geocit134")
        
    # relatives
    with Cluster(" "):
        server_c = EC2("CentOS")
        psql = Postgresql()

        server_c - Edge(label="contain") >> psql

    with Cluster(""):
        server_u = EC2("Ubuntu")
        geo = Custom("", "./img/geocitizen.png")

        server_u - Edge(label="contain") >> geo

    geo - Edge(color="blask", style="dashed") - psql

    # orchestration
    jenkins >> Edge(style="bold", color="red") \
            >> [terraform, ansible]
    
    terraform >> Edge(style="dotted") \
                >> jenkins

    # provisioning
    ansible >> Edge(label="config", color="black", style="bold") \
            >> [psql, geo]

    ansible >> Edge(label="get project", style="dashed") << github

    # building
    terraform >> Edge(label="create", color="mediumslateblue", style="bold") \
            >> [server_c,
                server_u]
