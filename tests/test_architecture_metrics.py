import io
import os
import unittest.mock

import pyjak.architecture_metrics as am
from pyjak.code_module import CodeModule

RESOURCES = os.path.join(os.path.dirname(__file__), "resources")
A_PACKAGE = os.path.join(RESOURCES, "com", "test", "a_package")
ANOTHER_PACKAGE = os.path.join(RESOURCES, "com", "test", "another_package")
WOW_YET_ANOTHER_PACKAGE = os.path.join(RESOURCES, "com", "test", "wow_yet_another")
ENCODING = "utf-8"


class TestArchitectureMetrics(unittest.TestCase):
    def setUp(self):
        self.module = CodeModule(am.scan_directory(RESOURCES, ENCODING))
        self.parser = am.create_parser()

    def check_console_output_for_lines_of_code(self, mock_stdout):
        with open(os.path.join(RESOURCES, "expected_console_output_for_lines_of_code.txt"), "r") as f:
            expected_lines = f.read().split("\n")
        actual_lines = mock_stdout.getvalue().split("\n")
        for line in expected_lines:
            if line not in actual_lines:
                self.fail(
                    f"An expected console line is different (or missing) :\n >{line}\n\n>{mock_stdout.getvalue()}")
        number_of_code_lines = [line.split()[1] for line in actual_lines if len(line.split()) >= 1]
        self.assertEqual(sorted(number_of_code_lines), number_of_code_lines,
                         "Printed lines are not ordered by length of the source files")

    def check_console_output_for_lines_of_code_several_modules(self, mock_stdout):
        with open(os.path.join(RESOURCES, "expected_console_output_for_lines_of_code_several_modules.txt"), "r") as f:
            expected_lines = f.read().split("\n")
        actual_lines = mock_stdout.getvalue().split("\n")
        for line in expected_lines:
            if line not in actual_lines:
                self.fail(
                    f"An expected console line is different (or missing) :\n >{line}\n\n >{mock_stdout.getvalue()}<")

    @unittest.mock.patch('sys.stderr', new_callable=io.StringIO)
    def test_parser_no_arguments(self, mock_stderr):
        with self.assertRaises(SystemExit):
            try:
                self.parser.parse_args([])
            except SystemExit as e:
                self.assertIn("usage:", mock_stderr.getvalue(), "Running without arguments does not display the usage")
                raise e

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_parser_directory_only(self, mock_stdout):
        args = self.parser.parse_args(["-m", RESOURCES])
        am.main_from_args(args)
        self.check_console_output_for_lines_of_code(mock_stdout)

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_parser_directory_and_encoding(self, mock_stdout):
        args = self.parser.parse_args(["-m", RESOURCES, "--encoding", ENCODING])
        am.main_from_args(args)
        self.check_console_output_for_lines_of_code(mock_stdout)

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_parser_several_directories(self, mock_stdout):
        args = self.parser.parse_args(["-m", A_PACKAGE, "-m", ANOTHER_PACKAGE, "-m", WOW_YET_ANOTHER_PACKAGE])
        print(args.module)
        am.main_from_args(args)
        self.check_console_output_for_lines_of_code_several_modules(mock_stdout)

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_analyze(self, mock_stdout):
        am.analyze([RESOURCES], ENCODING)
        self.check_console_output_for_lines_of_code(mock_stdout)

    def test_scan_directory(self):
        self.assertEqual(9, len(self.module.source_files), "Incorrect number of source files detected while scanning the directory")

    def test_build_imports_inside_module(self):
        self.assertEqual({'com.test.a_package.ClassWithImports': 0,
                          'com.test.a_package.ClassWithoutImport': 0,
                          'com.test.a_package.HelloWorld': 0,
                          'com.test.another_package.ClassWithImports': 0,
                          'com.test.another_package.ClassWithoutImport': 3,
                          'com.test.another_package.HelloWorld': 3,
                          'com.test.wow_yet_another.ClassWithImports': 0,
                          'com.test.wow_yet_another.ClassWithoutImport': 0,
                          'com.test.wow_yet_another.HelloWorld': 3},
                         self.module.internal_imports)

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_console_output_by_loc(self, mock_stdout):
        am.console_output_by_loc(self.module)
        self.check_console_output_for_lines_of_code(mock_stdout)


if __name__ == '__main__':
    unittest.main()
