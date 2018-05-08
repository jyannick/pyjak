import os

from gooey import Gooey, GooeyParser

from pyjak.entities import java_source_file
from pyjak.entities.component import Component

DEFAULT_ENCODING: str = "utf-8"


@Gooey(program_name="Pyjak", terminal_font_family="Courier", default_size=(1500, 800))
def main():
    parser = create_parser()
    args = parser.parse_args()
    main_from_args(args)


def main_from_args(args):
    analyze(args.module, args.encoding)


def create_parser():
    parser = GooeyParser()
    parser.add_argument("-m", "--module", action="append", required=True,
                        help="directory containing the source code to analyze",
                        widget="DirChooser")
    parser.add_argument("--encoding", action="store", default=DEFAULT_ENCODING,
                        help=f"encoding of the source files (default {DEFAULT_ENCODING})")
    return parser


def analyze(directories, encoding=DEFAULT_ENCODING):
    for directory in directories:
        if len(directories) > 1:
            print(f"\nAnalyzing module in directory {directory}")
        module = Component(scan_directory(directory, encoding))
        console_output_by_loc(module)


def scan_directory(directory, encoding):
    sources = set()
    for root, dirs, files in os.walk(directory):
        for name in files:
            file = os.path.join(root, name)
            if java_source_file.is_java_source_file(file):
                sources.add(java_source_file.JavaSourceFile(file, encoding))
    return sources


def console_output_by_loc(module):
    sources_by_loc = sorted(module.source_files, key=lambda s: s.lines_of_code)
    for source in sources_by_loc:
        print('\t'.join([f"{source.qualified_name:100}",
                         f"{(source.lines_of_code/1000):10.3f} kSLOC",
                         f"{source.number_of_imports:5} imports",
                         f"{module.internal_imports[source.qualified_name]:5} times imported inside module"]))


if __name__ == '__main__':
    main()
