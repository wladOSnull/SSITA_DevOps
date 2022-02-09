#!/bin/bash

### get the all arg1 file from arg2 folder and print them all 
pwd_file=`find ${1} -name ${2}`
echo -e "\n${pwd_file[@]}"

### split the string of results into the array
IFS=$'\n' read -rd '' -a pwd_file_array <<< "$pwd_file"
unset IFS

### print a final message with lenght (number of files) of the array 
echo -e "\nNumber of '${2}' files in '${1}' folder - ${#pwd_file_array[@]}"

<<USAGE

Execute this script:
~ ./7.sh ~/.vscode/ readme.*
~ ./7.sh /usr/local/go README.*
~ ./7.sh ~/.vscode/ README-*

Find README files with bash:
~ find ~ -name README
~ find /snap/snowflake -name README

Find reamde.* files with bash:
~ find ~/.vscode/ -name readme.*
~ find /usr/share/doc -name readme.*

Find README.* files with bash:
~ find /usr/local/go -name README.*

USAGE