#!/bin/env python


# --------------------
# System wide imports
# -------------------

import logging
import functools

# Typing hints
from argparse import ArgumentParser, Namespace
from typing import Sequence, Tuple

# ---------------------
# Third party libraries
# ---------------------

from lica.cli import execute
from lica.jinja2 import render_from

from .. import __version__
from ..common import parser as prs
from ..common.madmom import read_downbeat_markers, Marker

# ---------
# CONSTANTS
# ---------

TEMPLATE = "reaper.j2"

# -----------------------
# Module global variables
# -----------------------

log = logging.getLogger(__name__)
package = __name__.split(".")[0]
render = functools.partial(render_from, package)

# ==================
# AUXILIAR FUNCTIONS
# ==================


def to_reaper(item: Tuple[int, Marker]) -> Marker:
    i, marker = item
    marker["timestamp"] = marker["timestamp"].strftime("%H:%M:%S.%f")
    marker["beat"] = "M" if marker["beat"] == 1 else "B"
    marker["id"] = f"M{i}"
    return marker


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
    markers = list(map(to_reaper, enumerate(markers,start=1)))
    context = {"markers": markers, "howmany": len(markers)}
    rendered = render(TEMPLATE, context)
    with open(opath, "w") as fd:
        fd.write(rendered)
    log.info("Generated new Project Markers on file %s", opath)
  


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
        parents=[prs.ifile(), prs.oreaper()],
        help="Generate Reaper Project markers",
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
        description="Generate Reaper Project markers",
    )


if __name__ == "__main__":
    main()
