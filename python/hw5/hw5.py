import os, sys, sqlite3

### vars
##################################################
db_file1 = 'hw5_example.db'
db_file2 = 'demo.db'
db = os.path.join(os.path.dirname(__file__), db_file2)

conn = sqlite3.connect(db)
cur = conn.cursor()

serv_port = sys.argv[1]
serv_proj = sys.argv[2]
serv_name = sys.argv[3]

### functions
##################################################
def pretty_print(arg_result, arg_message):

    print(arg_message)

    for row in arg_result:
        print('{:5d} {:10s} {:10s}'.format(row[0], row[1], row[2]))

def server_ports():
    
    print("\nServerPorts tables: ")
    result = conn.execute("SELECT * FROM ServerPorts").fetchall()

    for i in result:
        print(i)
    
### SQL queries
##################################################

# SQL query for getting: (port + project + type) apache servers from Project3
sql1  = '''SELECT port_number, proj_name, type_name  FROM ServerPorts        
        INNER JOIN Servers
        ON Servers.id = ServerPorts.servers_id
        INNER JOIN ServerTypes
        ON ServerTypes.id = Servers.servertypes_id
        INNER JOIN ServerProjects
        ON ServerProjects.servers_id = Servers.id
        INNER JOIN Projects
        ON Projects.id = ServerProjects.projects_id
        WHERE 
            Projects.proj_name = '{}'
            AND
            ServerTypes.type_name = '{}';'''.format(serv_proj, serv_name)

# SQL query for changing: all apache servers's ports to 443 from Project3
sql2 = '''UPDATE ServerPorts 
        SET port_number = {} 
        WHERE ServerPorts.id IN ( 
            SELECT ServerPorts.id FROM ServerPorts
            INNER JOIN Servers
            ON Servers.id = ServerPorts.servers_id
            INNER JOIN ServerTypes
            ON ServerTypes.id = Servers.servertypes_id
            INNER JOIN ServerProjects
            ON ServerProjects.servers_id = Servers.id
            INNER JOIN Projects
            ON Projects.id = ServerProjects.projects_id
            WHERE 
                Projects.proj_name = '{}'
                AND
                ServerTypes.type_name = '{}');'''.format(serv_port, serv_proj, serv_name)

### updating + printing
##################################################

### ServerPorts tables
server_ports()

### current condition of ports
result = conn.execute(sql1).fetchall()
pretty_print(result, "\nBefore UPDATE:")

### updating
cur.execute(sql2)

### ServerPorts tables
server_ports()

### after updating
result = conn.execute(sql1).fetchall()
pretty_print(result, "\nAfrer UPDATE:")

### end
##################################################

### commiting / saving / applying all changes performed by cur (cursor)
conn.commit()

### connection closing
conn.close()

### usage + info
##################################################
'''
Executing this script:
~ python3 hw5.py 80 Project3 apache

Site for interaction with SQLite DB:
https://inloop.github.io/sqlite-viewer/#

Additional SQL queries for getting general info:
q1 = "SELECT name FROM sqlite_master WHERE type='table';"
q2 = "PRAGMA table_info(Servers);"
q3 = "SELECT * FROM Servers;"
q4 = "SELECT name FROM pragma_table_info('Servers') ORDER BY cid;"

# SQL query for getting: (ports) all apache servers
sql5 = "SELECT port_number FROM ServerPorts        
        INNER JOIN Servers
        ON Servers.id = ServerPorts.servers_id
        INNER JOIN ServerTypes
        ON ServerTypes.id = Servers.servertypes_id
        WHERE ServerTypes.type_name = 'apache';"

# SQL query for getting: (dns) all servers from Project3
sql6 = "SELECT dns_name FROM Servers
        INNER JOIN ServerProjects
        ON ServerProjects.servers_id = Servers.id
        INNER JOIN Projects
        ON Projects.id = ServerProjects.projects_id
        WHERE Projects.proj_name = 'Project3';"

# SQL query for getting: (port + dns) all servers
sql7 = "SELECT port_number, dns_name FROM ServerPorts
        INNER JOIN Servers
        ON Servers.id = ServerPorts.servers_id;"
'''