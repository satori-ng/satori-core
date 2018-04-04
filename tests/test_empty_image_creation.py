import unittest

from satoricore.image import SatoriImage

# python -m unittest  discover -v

class test_EmptyImage(unittest.TestCase):

    # def setUp(self):
    #     pass


    def test_create_image(self):
        si = SatoriImage()

        # si._test_print()
        self.assertTrue(True)

    def test_add_file(self):
        si = SatoriImage()

        si.add_file("/etc/shadow")
        ret = si.get_dir_contents("/etc")
        self.assertTrue('shadow' in ret)


    def test_isdir(self):
        si = SatoriImage()
        si.add_file("/etc/shadow")
        # ret = si.get_dir_contents("/etc")

        self.assertTrue(si.path.isdir('/etc'))
        self.assertTrue(not si.path.isdir('/etc/shadow'))
