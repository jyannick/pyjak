import argparse
import os

from pyjak import java_source_file


def main(directory, encoding):
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
    default_encoding = "utf-8"
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", help="directory containing the source code to analyze")
    parser.add_argument("--encoding", action="store", default=default_encoding,
                        help=f"encoding of the source files (default {default_encoding})")
    args = parser.parse_args()
    main(args.directory, args.encoding)
