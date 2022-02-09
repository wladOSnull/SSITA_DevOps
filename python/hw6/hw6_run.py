import docker

### vars
##################################################
docker_url = 'unix:///var/run/docker.sock'
init_image = 'homework:6'

local_bind_f = '/home/wlados/Documents/SSITA/python/hw6'
host_bind_f = '/home/sync'

client = docker.APIClient(base_url=docker_url)

config = client.create_container(
#    detach=True, 
#    stdin_open=True, 
    command="/home/startup_nginx.sh",
    tty=True,
    image=init_image,
    ports=[80],
    host_config=client.create_host_config(
        port_bindings={
            80: 8080,
        },
        binds={
           local_bind_f : {'bind': host_bind_f, 'ro': False},
        }),
#    command="nginx"
)

result = client.start(container=config.get('Id'))

print(config.get('Id'))
print(result)

'''
~ python3 hw6_run.py

~ docker exec -it trusting_thompson bash
'''
