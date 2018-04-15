import json

from satoricore.serialize import Serializer


class SatoriJsoner(Serializer):
	_type ='JSON'

	def __init__(self, compress=True):
		super().__init__(compress=compress, suffix='.json')

	def dumps(self, data_struct):
		if self.compress:
			content_dump = bytes(
				json.dumps(data_struct,
					indent=0,
					separators=(',',':'),
					),
				'utf8'
				)
		else:
			content_dump = json.dumps(data_struct)

		# content_dump = bytes(json.dumps(data_struct), 'utf8')
		return content_dump

	def loads(self, content):
		print (type(content))
		return json.loads(content)