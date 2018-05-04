import json

from satoricore.file import Serializer


class SatoriJsoner(Serializer):
	_type ='JSON'

	def __init__(self, compress=True):
		super().__init__(compress=compress, suffix='.json')

	def dumps(self, data_struct):
		if self.compress:
			content_dump = json.dumps(
					data_struct,
					indent=0,
					separators=(',',':'),
					)
				
		else:
			content_dump = json.dumps(data_struct)

		# print(content_dump)
		return bytes(content_dump, 'utf8')

	def loads(self, content):
		# print (type(content))
		# print(content)
		return json.loads(content)