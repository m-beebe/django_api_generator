import click
from . import utilities
from .api_generator import APIGenerator

@click.command(
    context_settings={"ignore_unknown_options": True},
    help='Convert the class within the SOURCE_FILE.py into a Django API'
)
@click.argument('source_file', type=click.Path(exists=True))
def generate_api(source_file):
    print('DJANGO API GENERATOR')

    utilities.file_is_python(source_file)
    exit()


    module_name = source_file.split('.')[0]
    
    module = __import__(module_name)

    class_for_api = getattr(module, module_name)()
    
    APIGenerator(class_for_api)
    

    