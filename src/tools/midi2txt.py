import pathlib
import click
from pathlib import Path, PurePath

@click.command()
@click.argument('filename')
def read(filename):
    """ Read a bionary file and output it as readable text file."""
    file = Path(filename)
    if not file.is_file():
        click.echo('Unfortunatley {} is not a file'.format(filename))
        return -1

    absolute_filename = file.resolve()

    if not absolute_filename.suffix == '.mid':
        click.echo('Unfortunatley {} is not a MIDI file'.format(filename))
        return -1

    click.echo('stem : {}'.format(absolute_filename.stem))
    click.echo('parents : {}'.format(absolute_filename.parents[0]))

    output_filename = PurePath.joinpath(absolute_filename.parents[0],
                                        absolute_filename.stem+'.txt')

    click.echo(output_filename)
    output = open(output_filename, 'w')

    input = open(filename, 'rb')
    buf = bytes(input.read())
    padding = len(str(len(buf)))
    formatting = '{' + ':0>' + str(padding) + '}:'

    i = 0
    while i < len(buf):
        if len(buf)-i > 16:
            loop = 16
        else:
            loop = len(buf)-i

        output.write(formatting.format(i))
        j = 0
        while j < loop:
            h = str(hex(buf[i]))
            v = h[2:]
            output.write(' {:0>2}'.format(v))
            j += 1
            i += 1

        output.write('\n')

    input.close()
    output.close()

if __name__ == '__main__':
    read()
