import sys, deb_pkg_tools.package

### opening & inspecting .deb file 
##################################################
package = deb_pkg_tools.package.inspect_package_fields(sys.argv[1])

### printing specified fields from header
##################################################
print(package['Package'],
        package['Version'],
        sep='\n')

print("\n\n")

### printing all fields from header
##################################################
for element in package:
    print(element, '...........', package[element])

### usage
##################################################
'''
Executing this script:
~ python3 hw4_deb.py ...
'''
