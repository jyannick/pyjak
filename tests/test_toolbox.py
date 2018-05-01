import io
import unittest.mock

from pyjak import toolbox


class DummyClass(object):
    @toolbox.lazy_property
    def test_property(self):
        print("Computing value")
        return 42


class TestToolbox(unittest.TestCase):
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_lazy_property_value(self, mock_stdout):
        print("Instantiating dummy object : no computation occurs.")
        dummy = DummyClass()
        print("The value is computed only when needed")
        self.assertEqual(42, dummy.test_property)
        print("The value remains for subsequent calls, no computation occurs.")
        self.assertEqual(42, dummy.test_property)
        self.assertEqual("""Instantiating dummy object : no computation occurs.
The value is computed only when needed
Computing value
The value remains for subsequent calls, no computation occurs.
""", mock_stdout.getvalue())


if __name__ == '__main__':
    unittest.main()
