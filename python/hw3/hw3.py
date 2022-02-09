import os, sys, paramiko, time

### vars
##################################################
host_ip = sys.argv[1]
host_port = int(sys.argv[2])
host_login = sys.argv[3]
local_key = paramiko.RSAKey.from_private_key_file('./.ssh/id_rsa')

### functions
##################################################

### to create folders on host
def mkdir_on_host():
    host_path = sys.argv[4]
    obj_name = sys.argv[5]
    obj_number = int(sys.argv[6])
    obj_mod = sys.argv[7]

    host_path_full = os.path.join(host_path, obj_name)
    host_command = "mkdir -m " + obj_mod + ' ' + host_path_full

    print('command:', host_command, '\nnumber:' , obj_number)

    for iterator in range(obj_number):
        stdin, stdout, stderr = ssh.exec_command(host_command + str(iterator + 1))
        #print(stdout.read().decode('ascii'))

### to perform some bash command on host
def command_on_host():
    host_command = sys.argv[4]

    stdin, stdout, stderr = ssh.exec_command(host_command)
    print(stdout.read().decode('ascii'))
    #print(stdout.read())

### ssh configuration
##################################################
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

### ssh connection
##################################################
ssh.connect(host_ip, port=host_port, username=host_login, pkey=local_key)

### mkdir of other command
##################################################
if len(sys.argv) == 8:
    mkdir_on_host()
else:
    command_on_host()

### close ssh connection
##################################################
ssh.close()

### usage
##################################################
'''
Executing script / creating folders:
~ python3 hw3.py 192.168.56.2 22 vagrant /home/vagrant usr 5 050

Executing script / perform some bash commands:
~ python3 hw3.py 192.168.56.2 22 vagrant 'ls -l'
~ python3 hw3.py 192.168.56.2 22 vagrant 'chmod 551 usr*'
~ python3 hw3.py 192.168.56.2 22 vagrant 'rm -drf usr*'
'''