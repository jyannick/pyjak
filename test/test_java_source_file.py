import os
import unittest
from pyjak.java_source_file import JavaSourceFile, is_java_source_file

RESOURCES = "resources"
BASENAME_HELLO_WORLD = "HelloWorld.java"
BASENAME_WITH_IMPORTS = "ClassWithImports.java"
PACKAGE = os.path.join("com", "test", "a_package")
SOURCE_FILE_HELLO_WORLD = os.path.join(RESOURCES, PACKAGE, BASENAME_HELLO_WORLD)
SOURCE_FILE_WITH_IMPORTS = os.path.join(RESOURCES, PACKAGE, BASENAME_WITH_IMPORTS)
ENCODING = "utf-8"


class TestJavaSourceFile(unittest.TestCase):

    def setUp(self):
        self.hello_world = JavaSourceFile(SOURCE_FILE_HELLO_WORLD, ENCODING)
        self.class_with_imports = JavaSourceFile(SOURCE_FILE_WITH_IMPORTS, ENCODING)

    def test_init(self):
        self.assertEqual(SOURCE_FILE_HELLO_WORLD, self.hello_world.file)
        self.assertEqual(ENCODING, self.hello_world.encoding)

    def test_basename(self):
        self.assertEqual(BASENAME_HELLO_WORLD, self.hello_world.basename)

    def test_directory_name(self):
        self.assertEqual(os.path.join(RESOURCES, PACKAGE), self.hello_world.directory_name)

    def test_qualified_name(self):
        self.assertEqual("com.test.a_package.HelloWorld", self.hello_world.qualified_name)

    def test_class_name(self):
        self.assertEqual("HelloWorld", self.hello_world.class_name)

    def test_package(self):
        self.assertEqual("com.test.a_package", self.hello_world.package)

    def test_imports_empty(self):
        self.assertEqual(0, self.hello_world.number_of_imports)
        self.assertEqual([], self.hello_world.imports)

    def test_imports_with_actual_imports(self):
        self.assertEqual(5, self.class_with_imports.number_of_imports)
        self.assertEqual(["java.io.InputStream",
                          "java.util.Scanner",
                          "com.test.another_package.HelloWorld",
                          "com.test.another_package.ClassWithoutImport",
                          "com.test.wow_yet_another.HelloWorld"],
                         self.class_with_imports.imports)

    def test_lines_of_code(self):
        self.assertEqual(7, self.hello_world.lines_of_code)

    def test_real_code_lines_and_comments_filtering(self):
        self.assertEqual(['package com.test.a_package;',
                          'public class HelloWorld',
                          '{',
                          '\tpublic static void main(String[] args) {',
                          '\t\tSystem.out.println("Hello World!");',
                          '\t}',
                          '}'],
                         self.hello_world._real_code_lines)

    def test_is_java_source_file(self):
        self.assertEqual(True, is_java_source_file(SOURCE_FILE_HELLO_WORLD))

if __name__ == '__main__':
    unittest.main()
