#!/bin/env python


# --------------------
# System wide imports
# -------------------

import logging
import functools

# Typing hints
from argparse import ArgumentParser, Namespace
from typing import Sequence, Dict, Any

# ---------------------
# Third party libraries
# ---------------------

from lica.cli import execute
from lica.jinja2 import render_from

from .. import __version__
from ..common import parser as prs
from ..common.madmom import read_downbeat_markers

# ---------
# CONSTANTS
# ---------

TEMPLATE = "transcribe.j2"
HEADER = ("timestamp", "beat")

Marker = Dict[str, Any]
Markers = Sequence[Marker]

# -----------------------
# Module global variables
# -----------------------

log = logging.getLogger(__name__)
package = __name__.split(".")[0]
render = functools.partial(render_from, package)

# ==================
# AUXILIAR FUNCTIONS
# ==================


def to_transcribe(item: Marker) -> Marker:
    item["timestamp"] = item["timestamp"].strftime("%H:%M:%S.%f")
    item["beat"] = "M" if item["beat"] == 1 else "B"
    return item


def append_to_file(path: str, markers: str) -> None:
    with open(path, "a") as fd:
        fd.write("\n")
        fd.write(markers)


def edit_file(path: str, lines: Sequence[str], markers: str) -> None:
    cut_point = dict()
    for i, line in enumerate(lines):
        if line.startswith("SectionStart,Markers"):
            cut_point["IN"] = i
        elif line.startswith("SectionEnd,Markers"):
            cut_point["OUT"] = i
    before = lines[: cut_point["IN"] - 1]
    after = lines[cut_point["OUT"] + 1 :]
    with open(path, "w") as fd:
        fd.writelines(before)
        fd.write(markers)
        fd.writelines(after)


def cli_generate(args: Namespace) -> None:
    ipath = args.input_file
    opath = args.output_file
    markers = read_downbeat_markers(ipath)
    markers = list(map(to_transcribe, markers))
    context = {"markers": markers, "howmany": len(markers)}
    rendered = render(TEMPLATE, context)
    with open(opath, "r") as fd:
        lines = fd.readlines()
    if any(line.startswith("SectionStart,Markers") for line in lines):
        log.info("Updating Markers section on file %s", args.output_file)
        edit_file(args.output_file, lines, rendered)
        msg = "Edited"
    else:
        log.info("Adding new Markers section on file %s", args.output_file)
        append_to_file(opath, rendered)
        msg = "Appended"
    bars = [m for m in markers if m["beat"] == "M"]
    beats = [m for m in markers if m["beat"] == "B"]
    log.info("%s %d bar markers & %d beat markers", msg, len(bars), len(beats))


# ========================
# MAIN ENTRY POINT PARSERS
# ========================


# ===================================
# MAIN ENTRY POINT SPECIFIC ARGUMENTS
# ===================================


def add_args(parser: ArgumentParser) -> None:
    subparser = parser.add_subparsers(dest="command", required=True)
    # ---------------------------------------------------------------
    parser = subparser.add_parser(
        "generate",
        parents=[prs.ifile(), prs.otranscribe()],
        help="Generate Tempo markers fron Transcribe! (c) software",
    )
    parser.set_defaults(func=cli_generate)


# ================
# MAIN ENTRY POINT
# ================


def cli_main(args: Namespace) -> None:
    args.func(args)


def main():
    execute(
        main_func=cli_main,
        add_args_func=add_args,
        name=__name__,
        version=__version__,
        description="Generate Transcribe! beat/downbeat markers",
    )


if __name__ == "__main__":
    main()
