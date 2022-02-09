#!/bin/bash

### simple regex for checking contained 'arg' anywhere
regex="^(${1})"
# counter for number of 'arg' string
counter=0

echo

### reading file line by line
while IFS= read -r line
do
    ### validating current string
    if [[ ! $line =~ $regex ]]
    then
        ### increment counter
        ((counter+=1))
        
        ### output current 'arg' string
        echo "${line}"
    fi   
done < $2

unset IFS

### the result of text processing
echo -e "\ncount of '${1}' in - ${2}: ${counter}\n"

<<USAGE

Executing this script:
~ ./6.sh daemon /etc/group
~ ./6.sh systemd /etc/group
~ ./6.sh pulse /etc/group

USAGE