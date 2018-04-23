import os
import re

from pyjak.toolbox import lazy_property


class JavaSourceFile:
    def __init__(self, file, encoding):
        self.file = file
        self.encoding = encoding

    @lazy_property
    def basename(self):
        return os.path.basename(self.file)

    @lazy_property
    def directory_name(self):
        return os.path.dirname(self.file)

    @lazy_property
    def qualified_name(self):
        return f"{self.package}.{self.class_name}"

    @lazy_property
    def class_name(self):
        return self.basename.replace(".java", "")

    @lazy_property
    def package(self):
        for line in self._real_code_lines:
            match = re.match(r"package ([\w.]*);", line)
            if match:
                return match.group(1)
        else:
            return "(no package found)"

    @lazy_property
    def imports(self):
        imports = list()
        for line in self._real_code_lines:
            match = re.match(r"import ([\w.]*);", line)
            if match:
                imports.append(match.group(1))
        return imports

    @lazy_property
    def number_of_imports(self):
        return len(self.imports)

    @lazy_property
    def lines_of_code(self):
        return len(self._real_code_lines)

    @lazy_property
    def _real_code_lines(self):
        with open(self.file, 'r', encoding=self.encoding) as f:
            content = f.read()
        code_content = remove_empty_lines(remove_block_comments(remove_inline_comments(content)))
        lines = code_content.split('\n')
        if lines[-1] == '':
            return lines[:-1]
        else:
            return lines


def is_java_source_file(file):
    return file.endswith(".java")


def remove_block_comments(content):
    return re.sub(r"/\*.*?\*/", "", content, flags=re.DOTALL)


def remove_inline_comments(content):
    return re.sub(r"\s*?//.*?\n", "\n", content)


def remove_empty_lines(content):
    return re.sub(r"^\s*?[\r\n]", "", content, flags=re.MULTILINE)
