import os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

file_name = None # contents are written in this file during the session
create_abs_path = lambda file_name : os.path.join(THIS_FOLDER, file_name)

def create_output_file_name():
    # if global file_name is already created in this session, then use it
    global file_name
    if file_name: return file_name

    default_file_name = 'output.txt'
    name = default_file_name

    i = 1
    while os.path.exists(create_abs_path(name)):
        name = f'{i}-{default_file_name}'
        i += 1
    
    file_name = name

    return name

def get_line_count_in_file(file):
    line_count = None
    try:
        file = open(file, "r")
        nonempty_lines = [line.strip("\n") for line in file if line != "\n"]

        line_count = len(nonempty_lines)
        file.close()
    except Exception as e:
        print('Error:', str(e))

    return line_count