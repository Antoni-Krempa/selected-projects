import os
from config import CHARACTER_LIMIT
from google import genai
from google.genai import types


schema_get_file_content = types.FunctionDeclaration(
            name="get_file_content",
            description="Prints first 10000 chars of the content of the file in a specified directory relative to the working directory",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "file_path": types.Schema(
                        type=types.Type.STRING,
                        description="This specific string should be the name or path of the file I want to open.",
                    ),
                },
                required=["file_path"],
            ),
        )


def get_file_content(working_directory, file_path):
    try:

        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # Will be True or False
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        if valid_target_dir == False:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if os.path.isfile(target_dir) == False:
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        with open(target_dir, "r") as f:
            final_string = f.read(CHARACTER_LIMIT)
            # After reading the first MAX_CHARS...
            if f.read(1):
                final_string += f'[...File "{file_path}" truncated at {CHARACTER_LIMIT} characters]'
            return final_string
        


    except Exception as e:
        return f"Error: {e}"