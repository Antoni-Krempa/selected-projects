import os
from google import genai
from google.genai import types


schema_write_file = types.FunctionDeclaration(
            name="write_file",
            description="Writes content to the file in specified directory",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "file_path": types.Schema(
                        type=types.Type.STRING,
                        description="This specific string should be the name or path of the file I want to write content to.",
                    ),
                    "content": types.Schema(
                        type=types.Type.STRING,
                        description="This string should be the content i want write into a file",
                    ),
                },
                required=["file_path","content"],
                
            ),
        )


def write_file(working_directory, file_path, content):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # Will be True or False
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        if valid_target_dir == False:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(target_dir):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        parent = os.path.dirname(target_dir)
        os.makedirs(parent, exist_ok=True)

        with open(target_dir, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"

