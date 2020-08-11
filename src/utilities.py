import click

def file_is_python(filename):
    try:
        extension = filename.split('.')[-1]
        if extension != 'py':
            raise IOError(f'Source file must be a Python file (.py, not .{extension})')

    except IOError as error:
        click.echo(error)
