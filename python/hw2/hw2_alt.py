import os, sys, json

### vars
##################################################

picked_object = {}
single_json_result = {}
list_result = []
list_files = os.listdir(path=sys.argv[1])

### functions
##################################################

def search_biggest_ei(arg_data):
    
    biggest_number = 0.0
    
    for matrix_element in arg_data['matrix']:
    
        if int(matrix_element['result']) != 0 and float(matrix_element['number']) >= float(biggest_number):

            picked_object['id'] = matrix_element['id']
            picked_object['number'] = matrix_element['number']
            picked_object['committer_name'] = arg_data['committer_name']
            picked_object['committer_email'] = arg_data['committer_email']
            #####
            #picked_object['result'] = matrix_element['result']
        
            biggest_number = matrix_element['number']

def search_biggest_2c(arg_data):

    biggest_number = 0.0
    object_id = 0

    for matrix_element in arg_data['matrix']:
        
        if int(matrix_element['result']) != 0 and float(matrix_element['number']) >= float(biggest_number):

            object_id = matrix_element['id']
            biggest_number = matrix_element['number']

    for matrix_element in arg_data['matrix']:

        if int(matrix_element['id']) == object_id:
            
            picked_object['id'] = matrix_element['id']
            picked_object['number'] = matrix_element['number']
            picked_object['committer_name'] = arg_data['committer_name']
            picked_object['committer_email'] = arg_data['committer_email']
            #####
            #picked_object['result'] = matrix_element['result']

def parser_json(arg_file):

    path_to_parsed = os.path.join(sys.argv[1], arg_file)

    with open(path_to_parsed, 'r') as parsed_file:
        parsed_data = json.load(parsed_file)
      
        search_biggest_ei(parsed_data)
        #search_biggest_2c(parsed_data)

    single_json_result[arg_file] = picked_object.copy()
    list_result.append(single_json_result.copy())
    single_json_result.clear()

### main
##################################################

with open(sys.argv[2], 'w') as output_file:

    for input_file in list_files:
        #print(input_file)
        parser_json(input_file)
    
    json.dump(list_result, output_file, indent=4, sort_keys=False)

### usage
##################################################
'''
Executing script / parsing folder with .json files:
~ python3 hw2_alt.py ./json/ result_alt.json
'''