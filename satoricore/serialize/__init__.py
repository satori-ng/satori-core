from satoricore.image import SatoriImage

class Serializer(object):
	def __init__(self, compress=False, suffix=''):
		self.suffix = suffix
		self.open = open
		self.compress = compress
		self.last_file = None
		if compress == True:
			import gzip
			self.open = gzip.open
			self.suffix += '.gz'

	def write(self, image, filename):
		filename += self.suffix
		data_struct = image._get_data_struct()
		serialized = self.dumps(data_struct)
		fd = self.open(filename, 'wb')
		try:
			fd.write(serialized)
		except TypeError:
			fd.write(str(serialized))
		finally:
			fd.close()
		self.last_file = filename

	def read(self, filename, suffixed=True):
		if not suffixed:
			filename += self.suffix

		fd = self.open(filename, 'rb')
		content = fd.read()
		data_struct = self.loads(content)
		fd.close()
		image = SatoriImage()
		image._set_data_struct(data_struct)
		self.last_file = filename
		return image
