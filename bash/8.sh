#!/bin/bash

find ~ -maxdepth 1 -cmin -600 -type f

<<USAGE

CLI command for - printing sorted files ONLY (hidden too) in currretn directory by descending last modified time:

ls - list all visible files
-l - list them with detail info
-p - append to end of folders name (in output) slash symbol - '/'
-a - list hidden files also
-t - sort them by last modified time (descending)
-r - reverse sorting (default is by name)
| - 'pipe' for stream redirection
grep - filter with condition
-v - exclude condition
/ - arg for condition

~ ls -lpat | grep -v /

##################################################

CLI command for - getting all files in current directory modified later than 10 hours skipping all subdirectories:

find - search specified file(s) in root of directory
~ - find in home directory
-maxdepth - 'depth' of searched files
1 - arg for -maxdepth - 1 stands for current level -> ignore all subdirectories in specified directory
-cmin - file's status was last changed less than, more than or exactly n minutes ago
-600 - arg for -cmin - 600 minutes

~ find . -maxdepth 1 -cmin -600

##################################################

-type - find only specified type of files
f - arg for -type - find only files (not directories, links ...)

~ find . -maxdepth 1 -cmin -600 -type f

USAGE
