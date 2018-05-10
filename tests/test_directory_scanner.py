import unittest
from pyjak.directory_scanner import DirectoryScanner
import os

from pyjak.entities.java_source_file import JavaSourceFile

RESOURCES = os.path.join(os.path.dirname(__file__), "resources")
PACKAGE = os.path.join("com", "test", "a_package")
PACKAGE_DIRECTORY = os.path.join(RESOURCES, PACKAGE)
BASENAME_WITH_IMPORTS = "ClassWithImports.java"
BASENAME_WITHOUT_IMPORTS = "ClassWithoutImports.java"
BASENAME_HELLO_WORLD = "HelloWorld.java"
SOURCE_FILE_WITH_IMPORTS = os.path.join(RESOURCES, PACKAGE, BASENAME_WITH_IMPORTS)
SOURCE_FILE_WITHOUT_IMPORTS = os.path.join(RESOURCES, PACKAGE, BASENAME_WITHOUT_IMPORTS)
SOURCE_FILE_HELLO_WORLD = os.path.join(RESOURCES, PACKAGE, BASENAME_HELLO_WORLD)


class TestDirectoryScanner(unittest.TestCase):
    def setUp(self):
        self.scanner = DirectoryScanner(PACKAGE_DIRECTORY)

    def test_init(self):
        self.assertEqual(PACKAGE_DIRECTORY, self.scanner.directory)

    def test_source_files(self):
        self.assertCountEqual(set([JavaSourceFile(SOURCE_FILE_WITH_IMPORTS),
                                   JavaSourceFile(SOURCE_FILE_WITHOUT_IMPORTS),
                                   JavaSourceFile(SOURCE_FILE_HELLO_WORLD)]), self.scanner.source_files)


if __name__ == '__main__':
    unittest.main()
