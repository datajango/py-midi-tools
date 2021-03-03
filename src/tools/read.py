import sys
import click
from pathlib import Path, PurePath
from src.midilib.midi_file import MidiFile

@click.command()
@click.argument('filename')
def read(filename):
    """ Read a midi file and output it as Readable text file."""
    file = Path(filename)
    if not file.is_file():
        click.echo('Unfortunatley {} is not a file'.format(filename))
        return -1

    absolute_filename = file.resolve()

    if not absolute_filename.suffix=='.mid':
        click.echo('Unfortunatley {} is not a MIDI file'.format(filename))
        return -1

    click.echo('stem : {}'.format(absolute_filename.stem))
    click.echo('parents : {}'.format(absolute_filename.parents[0]))

    output_filename = PurePath.joinpath(absolute_filename.parents[0],
                                       absolute_filename.stem+'.txt')

    click.echo(output_filename)

    mf = MidiFile()

    #try:
    mf.read(filename)
    mf.process()
    #except Exception as error:
    #    click.echo('Caught this error: ' + repr(error))


if __name__ == '__main__':
    if len(sys.argv)==1:
        arg = "./assets/a.mid"
        #arg = "midis/c.mid"
        sys.argv.append(arg)
    read()
