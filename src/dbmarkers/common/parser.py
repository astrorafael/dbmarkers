from argparse import ArgumentParser

from lica.validators import vfile

from .validators import vtranscribe, vreaper

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

def oreaper() -> ArgumentParser:
    parser = ArgumentParser(add_help=False)
    parser.add_argument(
        "-o",
        "--output-file",
        type=vreaper,
        required=True,
        metavar="<.csv File>",
        help="Reaper .csv project marker file",
    )
    return parser