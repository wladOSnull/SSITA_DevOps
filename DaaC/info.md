# DaaC

## Installation

- installing 'graphviz' via apt

  ```bash
  ~ sudo apt install graphviz
  ```

- installing 'diagrams' via pip3

  ```bash
  ~ pip3 install diagrams
  ```

## Sample

- creating python file

  ```bash
  ~ nano test.py
  ```

- using of demo code

  ```python
  from diagrams import Diagram
  from diagrams.aws.compute import EC2
  from diagrams.aws.database import RDS
  from diagrams.aws.network import ELB

  with Diagram("Web Service", show=False):
    ELB("lb") >> EC2("web") >> RDS("userdb")
  ```

- building diagrams

  ```bash
  ~ python3 test.py
  ```