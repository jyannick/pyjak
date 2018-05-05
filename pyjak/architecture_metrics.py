import os

from gooey import Gooey, GooeyParser

from pyjak import java_source_file

DEFAULT_ENCODING: str = "utf-8"


@Gooey(program_name="Pyjak", terminal_font_family="Courier", default_size=(1400, 800))
def main():
    parser = create_parser()
    args = parser.parse_args()
    main_from_args(args)


def main_from_args(args):
    analyze(args.directory, args.encoding)


def create_parser():
    parser = GooeyParser()
    parser.add_argument("directory", help="directory containing the source code to analyze", default=os.getcwd(),
                        widget="DirChooser")
    parser.add_argument("--encoding", action="store", default=DEFAULT_ENCODING,
                        help=f"encoding of the source files (default {DEFAULT_ENCODING})")
    return parser


def analyze(directory, encoding=DEFAULT_ENCODING):
    sources = scan_directory(directory, encoding)
    imports_inside_module = build_imports_inside_module(sources)
    console_output_by_loc(sources, imports_inside_module)


def scan_directory(directory, encoding):
    sources = set()
    for root, dirs, files in os.walk(directory):
        for name in files:
            file = os.path.join(root, name)
            if java_source_file.is_java_source_file(file):
                sources.add(java_source_file.JavaSourceFile(file, encoding))
    return sources


def build_imports_inside_module(sources):
    imports_inside_module = dict()
    for source in sources:
        imports_inside_module[source.qualified_name] = 0
    for source in sources:
        for import_ in source.imports:
            if import_ in imports_inside_module.keys():
                imports_inside_module[import_] += 1
    return imports_inside_module


def console_output_by_loc(sources, imports_inside_module):
    sources_by_loc = sorted(sources, key=lambda s: s.lines_of_code)
    for source in sources_by_loc:
        print('\t'.join([f"{source.qualified_name:100}",
                         f"{(source.lines_of_code/1000):10.3f} kLOC",
                         f"{source.number_of_imports:5} imports",
                         f"{imports_inside_module[source.qualified_name]:5} time imported"]))


if __name__ == '__main__':
    main()
