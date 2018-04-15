import os
import unittest

from satoricore.image import SatoriImage
from satoricore.serialize.pickle import SatoriPickler
from satoricore.serialize.json import SatoriJsoner


class test_Serializers(unittest.TestCase):

    def setUp(self):
        # filenames = os.random(4)
        self.image = SatoriImage()
        self.image.add_file("/etc/passwd")    # Add a file

        str_pkl_com = SatoriPickler()
        str_pkl = SatoriPickler(compress=False)

        str_jsn_com = SatoriJsoner()
        str_jsn = SatoriJsoner(compress=False)
        self.serializers = [
            str_jsn_com, str_jsn,
            str_pkl_com, str_pkl,
        ]

        try:
            os.mkdir("gen_images")
        except FileExistsError:
            pass
        os.chdir("gen_images")

        for serializer in self.serializers:
            serializer.write(self.image, 'test')
        os.listdir('.')


    def test_create_image(self):
        for serializer in self.serializers:
            image = serializer.read('test', suffixed=False)
            self.assertTrue(image == self.image)


    def tearDown(self):
        for filename in os.listdir('.'):
            os.unlink(filename)
            # print("Cleaning '%s'" % filename)
            pass
        os.chdir("..")
        os.rmdir('gen_images')
