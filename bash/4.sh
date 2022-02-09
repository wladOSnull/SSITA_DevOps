#!/bin/bash

### simple regex for checking contained 'arg' anywhere
regex="(.*${1}).*$"
# counter for number of 'arg' string
counter=0

echo

### reading file line by line
while IFS= read -r line
do
    ### validating current string
    if [[ $line =~ $regex ]]
    then
        ### increment counter
        ((counter+=1))
        
        ### output current 'arg' string
        IFS=$':' read -rd '' -a line_block <<< "$line"
        echo "${line_block[0]}"
    fi   
done < $2

unset IFS

### the result of text processing
echo -e "\ncount of '${1}' in - ${2}: ${counter}\n"

<<USAGE

Executing this script:
~ ./4.sh /bin/bash /etc/passwd

Without $ in regex -> find arg1 in an entire line the arg2:
~ ./4.sh sbin /etc/passwd

USAGE