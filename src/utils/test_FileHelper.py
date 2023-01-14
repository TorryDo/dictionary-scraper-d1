from unittest import TestCase

from src.utils.FileHelper import FileHelper


class TestFileHelper(TestCase):

    def test_create_file(self):
        ip1 = 'no_suffix_file'
        try:
            FileHelper.create_file(ip1)
        except FileExistsError:
            FileHelper.delete_file(ip1)
            FileHelper.create_file(ip1)

        curfile = FileHelper.is_existed(ip1)
        self.assertTrue(curfile == True)
        FileHelper.delete_file(ip1)

    def test_current_dir(self):
        ip1 = '../'
        ip2 = '../../raw/test_words.txt'
        rs0 = FileHelper.current_dir()
        rs1 = FileHelper.current_dir(ip1)
        rs2 = FileHelper.current_dir(ip2)
        print(f'current dir 0 = {rs0}')
        print(f'current dir 1 = {rs1}')
        print(f'current dir 2 = {rs2}')
        self.assertTrue(len(rs0) > 2)
        self.assertTrue(len(rs1) > 2)
        self.assertTrue(len(rs2) > 2)

    def test_is_file(self):
        ip1: str = 'test_file.txt'
        ip2: str = '../test_file.txt'

        try:
            FileHelper.create_file(ip1)
            FileHelper.create_file(ip2)
        except FileExistsError:
            FileHelper.delete_file(ip1)
            FileHelper.create_file(ip1)
            FileHelper.delete_file(ip2)
            FileHelper.create_file(ip2)

        expect_true = FileHelper.is_file(ip1)
        expect_true2 = FileHelper.is_file(ip2)
        expect_false = FileHelper.is_file(FileHelper.current_dir())

        self.assertTrue(expect_true)
        self.assertTrue(expect_true2)
        self.assertFalse(expect_false)
        FileHelper.delete_file(ip1)
        FileHelper.delete_file(ip2)

    def test_is_dir(self):
        expect_true = FileHelper.is_dir(FileHelper.current_dir())
        expect_false = FileHelper.is_dir('test_FileHelper.py')
        self.assertTrue(expect_true)
        self.assertFalse(expect_false)

    def test_is_existed(self):
        ip1 = 'test_file.txt'
        FileHelper.create_file(ip1)
        is_existed = FileHelper.is_existed(FileHelper.current_dir(f'/{ip1}'))

        self.assertTrue(is_existed)
        FileHelper.delete_file(FileHelper.current_dir(f'/{ip1}'))

    def test_children(self):
        children = FileHelper.children()
        print(children)
        self.assertTrue(len(children) > 0)

    def test_mkdir_rmdir(self):
        path = 'testdir'
        FileHelper.mkdir(path)
        expect_true = FileHelper.is_existed(path)
        self.assertTrue(expect_true)
        FileHelper.rmdir(path)

        expect_false = FileHelper.is_existed(path)
        self.assertFalse(expect_false)

    def test_write_text_file(self):
        data = 'hello im a text'
        path = 'test_write_text_file.txt'
        FileHelper.write_text_file(path, data)

        expect_true = FileHelper.read_file(path) == data
        self.assertTrue(expect_true)

        FileHelper.delete_file(path)

    def test_split_each_line(self):
        data = """hello
whole
hell
bound
fork
"""
        path = 'test_write_text_file.txt'
        FileHelper.write_text_file(path, data)

        read = FileHelper.split_each_line(path)
        print(read)
        expect_true = len(read) == 5
        self.assertTrue(expect_true)

        FileHelper.delete_file(path)

    def test_delete_file(self):
        path = 'test_write_text_file.txt'
        FileHelper.create_file(path)

        expect_true = FileHelper.is_existed(path)
        self.assertTrue(expect_true)
        FileHelper.delete_file(path)
        self.assertFalse(FileHelper.is_file(path))
