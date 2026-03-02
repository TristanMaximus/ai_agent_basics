import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    try:
        abs_path_work_dir = os.path.abspath(working_directory)
        full_file_path = os.path.normpath(os.path.join(abs_path_work_dir, file_path))
        valid_target_file = os.path.commonpath([abs_path_work_dir, full_file_path]) == abs_path_work_dir # check that file to read is inside work dir (our requirement guardrail)

        # go/green checks (path to file is inside workdir, file is a regular file and exists, file is a python file)
        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(full_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        # craft command to run python code
        command = ["python", full_file_path]
        if args != None:
            command.extend(args)

        run_result = subprocess.run(command, cwd = working_directory, capture_output = True, text = True, timeout = 30)
        string_result = ""

        # process error cases
        if run_result.returncode != 0:
            string_result += "Process exited with code X\n"
        if run_result.stdout == None and run_result.stderr == None:
            string_result += "No output produced\n"
        else:
            # process result output
            string_result += f"STDOUT: {run_result.stdout}\nSTDERR:{run_result.stderr}\n"

        return string_result
    except Exception as e:
        print(f"Caught error: {e}")
        return f"Error: executing Python file: {e}"
