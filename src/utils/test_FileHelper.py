from unittest import TestCase

from src.utils.FileHelper import FileHelper


class TestFileHelper(TestCase):

    def test_create_file(self):
        ip1 = 'no_suffix_file'
        rs = FileHelper.create_file(ip1)
        self.assertTrue(rs != '')

    def test_current_dir(self):
        test_input1 = '../'
        test_input2 = '../../raw/'
        cur_dir = FileHelper.current_dir()
        print(f'current dir = {cur_dir}')
        self.assertTrue(cur_dir != '' and cur_dir is not None)

    def test_is_file(self):
        input1 = '../../raw'
        self.fail()

    def test_is_dir(self):
        self.fail()

    def test_is_existed(self):
        ip1 = 'test_file.txt'
        FileHelper.create_file(ip1)
        is_existed = FileHelper.is_existed(FileHelper.current_dir(f'/{ip1}'))

        self.assertTrue(is_existed)
        FileHelper.delete_file(FileHelper.current_dir(f'/{ip1}'))

    def test_children(self):
        children = FileHelper.children(FileHelper.current_dir('/src/utils'))
        self.assertTrue(len(children) > 0)

    def test_is_empty_directory(self):
        self.fail()

    def test_write_text_file(self):
        self.fail()

    def test_split_each_line(self):
        self.fail()

    def test_delete_file(self):
        self.fail()
