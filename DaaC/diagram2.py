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

# entrypoint
with Diagram("Geocitizen 2",  filename="Geocitizen2", show=False):

    jenkins = Jenkins()
    ansible = Ansible()
    terraform = Terraform()
        
    # relatives
    with Cluster(" "):
        server_c = Server("CentOS")
        psql = Postgresql()

        server_c - psql

    with Cluster(""):
        server_u = Server("Ubuntu")
        geo = Custom("", "./img/geocitizen.png")

        server_u - geo

    geo - Edge(color="blask", style="dashed") - psql

    # orchestration
    jenkins >> Edge(style="bold", color="red") \
            >> [terraform, ansible]
    
    terraform >> Edge(style="dotted") \
                >> jenkins

    # provisioning
    ansible >> Edge(label="config", color="black", style="bold") \
            >> [psql, geo]

    # building
    terraform >> Edge(label="config", color="mediumslateblue", style="bold") \
            >> [server_c,
                server_u]
