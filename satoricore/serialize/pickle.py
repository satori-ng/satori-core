import pickle

from satoricore.serialize import Serializer


class SatoriPickler(Serializer):

	def __init__(self, compress=True):
		super().__init__()
		if compress == True:
			import gzip
			self.open = gzip.open


	def dumps(self, data_struct):
		return pickle.dumps(data_struct)



	def loads(self, content):
		return pickle.loads(content)