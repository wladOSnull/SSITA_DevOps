import os, sys, dockermap.api, docker

### vars
##################################################
docker_url = 'unix:///var/run/docker.sock'
init_image = sys.argv[1]
tag_name = sys.argv[2]
myhtml_path_local = sys.argv[3]
myhtml_path_container = '/usr/share/nginx/html/index.html'

"""

Creating the Docker image

"""

### loading into local Docker storage 
### the example image
##################################################
#os.system("docker load < {}".format(init_image))

### establish connection 
### + picking the available Docker image 
##################################################
docker_conn = dockermap.api.DockerClientWrapper(docker_url)
docker_file = dockermap.api.DockerFile('{}'.format(init_image), maintainer='SSTIA: python, homework #6')

### preconfiguring
##################################################

### installing necessary apps
docker_file.run_all('yum install -y epel-release')
docker_file.run_all('yum install -y nginx')
docker_file.run_all('yum clean all')

### provisioming with the web page
docker_file.add_file(myhtml_path_local, myhtml_path_container)

#docker_file.prefix('ENV', 'JAVA_HOME', '/usr/lib/jvm/java-openjdk')
#docker_file.prefix('ENV', 'PATH', '/opt/gradle-2.5/bin:$PATH')

### build Docker image
##################################################
docker_conn.build_from_file(docker_file, tag_name)

"""

Run the Docker container

"""

local_bind_f = '/home/wlados/Documents/SSITA/python/hw6'
host_bind_f = '/home/sync'

client = docker.APIClient(base_url=docker_url)

nginx_start = "/bin/bash nginx"
config = client.create_container(
    image=tag_name,
#    command=nginx_start,
    tty=True,
#    detach=True, 
#    stdin_open=True, 
    ports=[80],
    host_config=client.create_host_config(
        port_bindings={
            80: 8080,
        },
        binds={
           local_bind_f : {'bind': host_bind_f, 'ro': False},
        }
    )
)

client.start(container=config.get('Id'))

### usage
##################################################
'''
Execute this script:
~ python3 hw6.py centos7/hw homework:6 ./html/index.html

~ docker run -it --rm -d -p 8080:80 --name web homework:6
'''