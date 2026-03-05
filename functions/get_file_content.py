import os
from config import MAX_CHARS
from google.genai import types

# Function Declaration (or schema) for the LLM. We tell the LLM about functions we provide and how to use them
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Get contents of a an existing file located on the path relative to the working directory. Returns full contents if file contains less that {MAX_CHARS} characters. Truncated otherwise.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to a file to get content from, relative to the working directory.",
            ),
        },
        required=["file_path"]
    ),
)

def get_file_content(working_directory, file_path):
    try:
        abs_path_work_dir = os.path.abspath(working_directory)
        full_file_path = os.path.normpath(os.path.join(abs_path_work_dir, file_path))
        valid_target_dir = os.path.commonpath([abs_path_work_dir, full_file_path]) == abs_path_work_dir # check that file to read is inside work dir (our requirement guardrail)

        if not valid_target_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(full_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(full_file_path, "r") as file:
            contents = file.read(MAX_CHARS)
            # After reading the first MAX_CHARS. To confirm if we read the whole file or not
            if file.read(1):
                contents += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return contents
    except Exception as e:
        print(f"Caught error: {e}")
        return f'Error reading file "{file_path}": {e}'
