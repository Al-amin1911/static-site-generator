import unittest
import unittest
from src.main import extract_title

class TestMain(unittest.TestCase):
    def test_valid_title(self):
        md = """# My Title

This is a paragraph"""
        result = extract_title(md)
        self.assertEqual(result, "My Title")

    def test_no_title(self):
        md = """This is a paragraph

Another paragraph"""
        result = extract_title(md)
        self.assertIsNone(result)
    pass

if __name__ == "__main__":
    unittest.main()