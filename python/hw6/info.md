# Python

## Module 6. Homework

- Got permission denied while trying to connect to the Docker daemon socket ... :
  ```bash
  ~ sudo chmod 666 /var/run/docker.sock
  ```

- Install required module for python:
  ```bash
  ~ pip3 install docker
  ```
- Packing docker image into tar ball:
  ```bash
  ~ docker save <name-of-image>:latest | gzip > <name-of-archive>.tar.gz
  ```

- Loading example image from .tar archive:
  ```bash
  ~ docker image
  ~ docker load < <name-of-tar-archive>.tar
  ~ docker image
  ```

- Run simple nginx image and bind it's 80 port to host's 8080:
  ```bash
  ~ docker run -it --rm -d -p 8080:80 --name <name-for-container> <name-of-image>
  ```

- Accessing bash environment of an container:
  ```bash
  ~ docker exec -it <name-of-container> bash
  ```

- Work with images:
  ```bash
  ~ docker images
  ~ docker rmi <name-of-image>
  
  # delete all cache
  ~ docker system prune
  ```

- Get the dockermap.api module:
  ```bash
  ~ git clone https://github.com/merll/docker-map
  ~ cd docker-map
  ~ ls -1
  ~ pip3 install .
  ~ pip3 list | grep docker
  ```