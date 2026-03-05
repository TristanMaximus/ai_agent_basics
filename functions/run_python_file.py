import os
import subprocess
from google.genai import types

# Function Declaration (or schema) for the LLM. We tell the LLM about functions we provide and how to use them
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes code inside a python file (runs a python file) on the path relative to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to a python file to be executed. Path is relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Array/List of arguments to pass to the python file to run against.",
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Argument to pass to the python file."
                )
            )
        },
        required=["file_path"]
    ),
)

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
