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
with Diagram("Geocitizen 2",  filename="Geocitizen2", show=False):

    #github = Github("Geocit134")
    jenkins = Jenkins()
    ansible = Ansible()
    terraform = Terraform()

