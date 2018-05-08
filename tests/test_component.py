import os
import unittest
from pyjak.entities.component import Component
from pyjak.entities.java_source_file import JavaSourceFile

RESOURCES = os.path.join(os.path.dirname(__file__), "resources")
A_PACKAGE = os.path.join(RESOURCES, "com", "test", "a_package")
ANOTHER_PACKAGE = os.path.join(RESOURCES, "com", "test", "another_package")
WOW_YET_ANOTHER = os.path.join(RESOURCES, "com", "test", "wow_yet_another")
ENCODING = "utf-8"


class TestSoftwareComponent(unittest.TestCase):

    def setUp(self):
        self.a_component = Component(A_PACKAGE, JavaSourceFile)

    def test_init(self):
        self.assertEqual(["something"], self.a_component.source_files)