import json, sys

### prettifying of input .json file to get human-readable doc
##################################################

with open(sys.argv[1], 'r') as parsed_file:
    parsed_data = json.load(parsed_file)

    with open(sys.argv[2], 'w') as output_file:
        json.dump(parsed_data, output_file, indent=4, sort_keys=False)

### usage
##################################################
'''
Executing script / prettifying .json file:
~ python3 hw2_prettifier.py hw2_example.json pretty.json

Deleting created .json:
~ rm pretty.json
'''