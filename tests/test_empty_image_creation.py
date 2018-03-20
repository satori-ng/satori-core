import unittest

from satoricore.image import SatoriImage


class TestEmptyImage(unittest.TestCase):

    # def setUp(self):
    #     pass


    def test_create_image(self):
        si = SatoriImage()

        si._test_print()
        self.assertTrue(True)