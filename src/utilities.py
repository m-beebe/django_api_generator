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

<<<<<<< HEAD
def get_class(module, module_name):
    print(module, module_name)
    try:
        api_class = getattr(module, module_name)


    except AttributeError as error:
        click.echo(error)
        click.echo(
            f'Ensure that {module} contains a class named "{module_name}"'
        )
        exit()
    else:
        return api_class
    

def instantiate_class(class_name):
    try:
        instance = class_name()
    except AttributeError as error:
        click.echo(error)
    
    return instance
=======
def get_class(module, class_name)
>>>>>>> eb6d3ee41ad667aff1222a28a9245c3641dc73ac
