from satoricore.image import SatoriImage

class Serializer(object):

	def __init__(self):
		self.open = open


	def write(self, image, filename):
		data_struct = image._get_data_struct()
		serialized = self.dumps(data_struct)
		print(data_struct['data'])
		fd = self.open(filename, 'w')
		fd.write(serialized)
		fd.close()


	def read(self, filename):
		fd = self.open(filename)
		content = fd.read()
		data_struct = self.loads(content)
		fd.close()
		image = SatoriImage()
		image._get_data_struct()
		return image
