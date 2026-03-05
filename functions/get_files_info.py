import os
from google.genai import types

# Function Declaration (or schema) for the LLM. We tell the LLM about functions we provide and how to use them
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself). In case user asks about root, it is just a '.', meaning root of the working directory. Explicitly state root as '.'.",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    try:
        # we need to determine if directory we are looking at is inside our working_directory (LLM should only work inside working_dir) to guardrail LLM
        abs_path_work_dir = os.path.abspath(working_directory) # get absolute path of the working_dir
        # join absolute work dir path with directory, creating target_dir absolute path.
        # normpath deals with edge cases, like double slashes, .. (parent) etc.
        target_dir = os.path.normpath(os.path.join(abs_path_work_dir, directory))
        valid_target_dir = os.path.commonpath([abs_path_work_dir, target_dir]) == abs_path_work_dir # check that target dir is inside work dir (our requirement guardrail)
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir): # check that target is directory, so that we know we can list the contents
            return f'Error: "{directory}" is not a directory'
        contents = os.listdir(target_dir) # list files inside target dir
        print(f"{directory} contents: {contents}")
        result = list()
        for item in contents:
            full_item = os.path.normpath(os.path.join(target_dir, item))
            result.append(f"- {item}: file_size={os.path.getsize(full_item)} bytes, is_dir={os.path.isdir(full_item)}")
        return "\n".join(result)
    except Exception as e:
        return f"Error: {e}"
