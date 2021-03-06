import io
import os
import unittest.mock

import pyjak.architecture_metrics as am

RESOURCES = os.path.join(os.path.dirname(__file__), "resources")
ENCODING = "utf-8"


class TestArchitectureMetrics(unittest.TestCase):
    def setUp(self):
        self.sources = am.scan_directory(RESOURCES, ENCODING)
        self.imports_inside_module = am.build_imports_inside_module(self.sources)
        self.parser = am.create_parser()

    def check_console_output(self, mock_stdout):
        with open(os.path.join(RESOURCES, "expected_console_output_for_lines_of_code.txt"), "r") as f:
            expected_lines = f.read().split("\n")
        actual_lines = mock_stdout.getvalue().split("\n")
        for line in expected_lines:
            if line not in actual_lines:
                self.fail(f"An expected console line is different (or missing) :\n >{line}")
        number_of_code_lines = [line.split()[1] for line in actual_lines if len(line.split()) >= 1]
        self.assertEqual(sorted(number_of_code_lines), number_of_code_lines,
                         "Printed lines are not ordered by length of the source files")

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
        args = self.parser.parse_args([RESOURCES])
        am.main_from_args(args)
        self.check_console_output(mock_stdout)

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_parser_directory_and_encoding(self, mock_stdout):
        args = self.parser.parse_args([RESOURCES, '--encoding', ENCODING])
        am.main_from_args(args)
        self.check_console_output(mock_stdout)

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_analyze(self, mock_stdout):
        am.analyze(RESOURCES, ENCODING)
        self.check_console_output(mock_stdout)

    def test_scan_directory(self):
        self.assertEqual(9, len(self.sources), "Incorrect number of source files detected while scanning the directory")

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
                         self.imports_inside_module)

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_console_output_by_loc(self, mock_stdout):
        am.console_output_by_loc(self.sources, self.imports_inside_module)
        self.check_console_output(mock_stdout)


if __name__ == '__main__':
    unittest.main()
