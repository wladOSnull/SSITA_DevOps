import sys, rpmfile

### opening .rpm file
##################################################
with rpmfile.open(sys.argv[1]) as rpm:

    ### printing all headers of the RPM file
    #print(rpm.headers.keys())

    ### printing only specified headers
    print(rpm.headers.get('name').decode('ascii'), 
            rpm.headers.get('release').decode('ascii'),
            rpm.headers.get('version').decode('ascii'),
            sep='\n')

    ### printing all headers + values        
    #for i in rpm.headers:
    #    print(i, rpm.headers[i])

    ### printing all files the .rpm file contains
    #for member in rpm.getmembers():
    #    print(member)

### usage
##################################################
'''
Executing this script:
~ python3 hw4.py ...

Installing default rpm module:
apt install python3-rpm
pip list | grep rpm

Installing third-praty rpm module:
pip install rpmfile
'''
