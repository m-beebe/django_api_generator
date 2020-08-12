import click
from pathlib import Path
from .utilities import (
    file_is_python,
    load_module,
    get_class,
    instantiate_class
)
from .api_generator import APIGenerator

@click.command(
    context_settings={"ignore_unknown_options": True},
    help='Convert the class within the SOURCE_FILE.py into a Django API'
)
@click.argument('source_file', type=click.Path(exists=True))
def generate_api(source_file):
    print('DJANGO API GENERATOR')

    file_is_python(source_file)

    module_path = Path(source_file).resolve()
    
    module_name = module_path.name.split('.')[0]

    module = load_module(module_name)

    class_for_api = get_class(module, module_name)

    instance = instantiate_class(class_for_api)

    APIGenerator(instance)
    

    