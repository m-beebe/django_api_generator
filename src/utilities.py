import click
from pathlib import Path

def file_is_python(filename:str):
    '''If the filename has the extension .py, return True. Otherwise, return False'''    
    try:
        extension = filename.split('.')[-1]
        if extension != 'py':
            raise IOError(f'Source file must be a Python file (.py, not .{extension})')

    except IOError as error:
        click.echo(error)
        return False

    return True

def load_module(module_name):
    try:
        
        module = __import__(module_name)
    except ModuleNotFoundError:
        click.echo(f'Cannot import module: {module_name}')
        click.echo('\ndjango_api_generator must be called from the directory\n' \
            'containing the file for which you want to generate an API.\n\n'\

            'Note: relative file paths are not supported.\n'\
            'e.g. ../../my_module.py'
        )
        return None
    
    return module

def get_class(module, class_name)