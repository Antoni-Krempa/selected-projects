import os
import subprocess
from google import genai
from google.genai import types


schema_run_python_file = types.FunctionDeclaration(
            name="run_python_file",
            description="Runs the python file from specified directory by using subprocess",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "file_path": types.Schema(
                        type=types.Type.STRING,
                        description="This specific string should be the name or path of the file I want to run.",
                    ),
                    "args": types.Schema(
                        type=types.Type.ARRAY,
                        description="an array of strings to optionally pass additionaly to command",
                        items=types.Schema(
                            type=types.Type.STRING,
                        )
                    ),
                },
                required=["file_path"],
                
            ),
        )

def run_python_file(working_directory, file_path, args=None):

    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # Will be True or False
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        absolute_file_path = os.path.abspath(os.path.join(working_directory, file_path))

        if valid_target_dir == False:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(absolute_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        if file_path[-3:] != ".py":
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", target_dir] 
        if args != None:
            command.extend(args)

        result = subprocess.run(command,capture_output=True,timeout=30,text=True,cwd=working_directory)

        result_string = ''

        if result.returncode != 0:
            result_string += f"Process exited with code {result.returncode}\n"
        if (result.stderr == '') and (result.stdout == ''):
            result_string += "No output produced\n"
        result_string += f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    
        return result_string

    except Exception as e:
        return f"Error: executing Python file: {e}"