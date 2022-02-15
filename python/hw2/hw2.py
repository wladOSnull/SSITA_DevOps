import os, sys, json

### vars
##################################################

picked_object = {}
list_result = []
list_files = os.listdir(path=sys.argv[1])

### functions
##################################################

# searching of json element with biggest non-zero element
def search_biggest_ei(arg_data):
    
    biggest_number = 0.0
    
    for matrix_element in arg_data['matrix']:
    
        if int(matrix_element['result']) != 0 and float(matrix_element['number']) >= float(biggest_number):

            picked_object['id'] = matrix_element['id']
            picked_object['number'] = matrix_element['number']
            picked_object['committer_name'] = arg_data['committer_name']
            picked_object['committer_email'] = arg_data['committer_email']
            #####
            picked_object['result'] = matrix_element['result']
        
            biggest_number = matrix_element['number']

# parsing one current document
def parser_json(arg_file):

    path_to_parsed = os.path.join(sys.argv[1], arg_file)

    with open(path_to_parsed, 'r') as parsed_file:
        
        # 'uploading' file to variable
        parsed_data = json.load(parsed_file)
      
        # searching of json item
        search_biggest_ei(parsed_data)

    # pushing copy of founded item into list
    list_result.append(picked_object.copy())

### main
##################################################

# opening arg file to write
with open(sys.argv[2], 'w') as output_file:
    
    # processing all files in specified folder
    for input_file in list_files:
        
        # parsing current file
        parser_json(input_file)
    
    # writing all founded json item into file
    json.dump(list_result, output_file, indent=4, sort_keys=False)

### usage
##################################################
'''
Executing script / parsing folder with .json files:
~ python3 hw2.py ./json/ result.json
'''