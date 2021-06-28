import argparse
from lacmus_data.tools import (
    merge,
    crop,
    visdrone2voc,
    create,
    resize,
    voc2csv
)

def add_parsers():
    parser = argparse.ArgumentParser(prog="./ld")
    subparser = parser.add_subparsers(title="lacmus data tools", metavar="")

    # Add your tool's entry point below.

    merge.add_parser(subparser)
    crop.add_parser(subparser)
    resize.add_parser(subparser)
    create.add_parser(subparser)
    visdrone2voc.add_parser(subparser)
    voc2csv.add_parser(subparser)

    # We return the parsed arguments, but the sub-command parsers
    # are responsible for adding a function hook to their command.

    subparser.required = True

    return parser.parse_args()


def main():
    """main entrypoint for ladd tools"""
    args = add_parsers()
    args.func(args)


if __name__ == "__main__":
    main()