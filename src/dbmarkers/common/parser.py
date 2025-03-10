from argparse import ArgumentParser

from lica.validators import vfile

from .validators import vtranscribe

def ifile() -> ArgumentParser:
    parser = ArgumentParser(add_help=False)
    parser.add_argument(
        "-i",
        "--input-file",
        type=vfile,
        required=True,
        metavar="<File>",
        help="CSV Downbeat markers input file",
    )
    return parser


def otranscribe() -> ArgumentParser:
    parser = ArgumentParser(add_help=False)
    parser.add_argument(
        "-o",
        "--output-file",
        type=vtranscribe,
        required=True,
        metavar="<.xsc File>",
        help="Transcribe XSC output file to update",
    )
    return parser