import os

from pyjak.entities import java_source_file
from pyjak.toolbox import lazy_property


class DirectoryScanner:
    def __init__(self, directory):
        self.directory = directory

    @lazy_property
    def source_files(self):
        sources = set()
        for root, dirs, files in os.walk(self.directory):
            for name in files:
                file = os.path.join(root, name)
                if java_source_file.is_java_source_file(file):
                    sources.add(java_source_file.JavaSourceFile(file))
        return sources
