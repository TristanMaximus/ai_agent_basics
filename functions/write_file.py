import os

def write_file(working_directory, file_path, content):
    try:
        abs_path_work_dir = os.path.abspath(working_directory)
        full_file_path = os.path.normpath(os.path.join(abs_path_work_dir, file_path))
        valid_target_dir = os.path.commonpath([abs_path_work_dir, full_file_path]) == abs_path_work_dir # check that file to read is inside work dir (our requirement guardrail)

        if not valid_target_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(full_file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(file_path, exist_ok=True) # make sure folders on the file_path exist

        with open(full_file_path, "w") as file:
            file.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        print(f"Caught error: {e}")
        return f'Error reading file "{file_path}": {e}'
