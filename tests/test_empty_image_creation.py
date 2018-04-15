import unittest

from satoricore.image import SatoriImage, FileNotFoundError, NotADirectoryError


class test_EmptyImage(unittest.TestCase):

    def setUp(self):
        self.si = SatoriImage()


    def test_add_file(self):
        si = SatoriImage()

        si.add_file("/etc/shadow")
        # print(si)
        ret = si.get_dir_contents("/etc")
        # print(ret)
        self.assertTrue('shadow' in ret)


    def test_non_existent_file(self):
        self.si.add_file("/etc/shadow")
        try:
            self.si.get_dir_contents('/asjnas')
        except FileNotFoundError:
            self.assertTrue(True)


    def test_multiple_files(self):
        si = SatoriImage()

        si.add_file("/etc/shadow")
        si.add_file("/etc/passwd")
        si.add_file("/etc/sudoers")
        con = si.get_dir_contents('/etc')
        self.assertTrue(len(con) == 3)
        self.assertTrue('shadow' in con)
        self.assertTrue('passwd' in con)
        self.assertTrue('sudoers' in con)


    def test_listing_non_dir(self):
        si = SatoriImage()

        si.add_file("/etc/shadow")
        try:
            con = si.get_dir_contents('/etc/shadow')
        except NotADirectoryError:
            self.assertTrue(True)
