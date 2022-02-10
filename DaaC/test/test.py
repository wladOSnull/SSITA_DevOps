from diagrams import Diagram
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB

from diagrams.onprem.database import Postgresql
import diagrams.onprem.database as dt
from diagrams.generic.os import LinuxGeneral

with Diagram("Web Service", show=False):
    ELB("lb") >> EC2("web") >> RDS("userdb")
    Postgresql("kek") >> dt.Scylla("kek2")
    Postgresql("kek1")
    Postgresql("kek2")
    dt.Cassandra("casa")
    LinuxGeneral("LG")