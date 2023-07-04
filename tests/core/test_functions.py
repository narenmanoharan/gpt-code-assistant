import unittest
import os
import tempfile
import shutil
from core.functions import get_file_tree

class TestGetFileTree(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Remove the directory after the test
        shutil.rmtree(self.test_dir)

    def create_test_files(self, file_paths):
        for file_path in file_paths:
            os.makedirs(os.path.dirname(os.path.join(self.test_dir, file_path)), exist_ok=True)
            with open(os.path.join(self.test_dir, file_path), 'w') as f:
                f.write("Test")

    def test_get_file_tree(self):
        file_paths = ['file1.py', 'subdir/file2.py', 'subdir/subsubdir/file3.py']
        self.create_test_files(file_paths)

        result = get_file_tree(self.test_dir)
        expected = [os.path.join(self.test_dir, file_path) for file_path in file_paths]

        self.assertEqual(set(result), set(expected), "get_file_tree did not return the expected files")

    def test_get_file_tree_with_max_depth(self):
        file_paths = ['file1.py', 'subdir/file2.py', 'subdir/subsubdir/file3.py']
        self.create_test_files(file_paths)

        result = get_file_tree(self.test_dir, max_depth=1)
        expected = [os.path.join(self.test_dir, 'file1.py'), os.path.join(self.test_dir, 'subdir/file2.py')]

        self.assertEqual(set(result), set(expected), "get_file_tree did not return the expected files when max_depth is set")


    def test_get_file_tree_ignored_folders(self):
        file_paths = ['file1.py', '__pycache__/file2.py', '.git/file3.py']
        self.create_test_files(file_paths)

        result = get_file_tree(self.test_dir)
        expected = [os.path.join(self.test_dir, 'file1.py')]

        self.assertEqual(set(result), set(expected), "get_file_tree did not ignore specified folders")


    def test_get_file_tree_ignored_files(self):
        file_paths = ['file1.py', 'file2.pyc', 'file3.json']
        self.create_test_files(file_paths)

        result = get_file_tree(self.test_dir)
        expected = [os.path.join(self.test_dir, 'file1.py')]

        self.assertEqual(set(result), set(expected), "get_file_tree did not ignore specified files")


    def test_get_file_tree_empty_dir(self):
        empty_subdir = os.path.join(self.test_dir, 'empty_subdir')
        os.mkdir(empty_subdir)

        result = get_file_tree(self.test_dir)
        expected = []

        self.assertEqual(result, expected, "get_file_tree did not return the expected result for a directory with an empty subdirectory")




if __name__ == "__main__":
    unittest.main()
