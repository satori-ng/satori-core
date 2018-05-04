import pickle

from satoricore.file import Serializer


class SatoriPickler(Serializer):
	_type ='pickle'

	def __init__(self, compress=True):
		super().__init__(compress=compress, suffix='.pkl')

	def dumps(self, data_struct):
		content_dump = pickle.dumps(data_struct)
		return content_dump

	def loads(self, content):
		try:
			data_struct = pickle.loads(bytes(content,'utf8'))
		except TypeError:
			data_struct = pickle.loads(content)
		return data_struct