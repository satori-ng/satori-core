import argparse
import json
import sys

from satoricore.file.pickle import SatoriPickler
from satoricore.file.json import SatoriJsoner


def display_image(image):
	data_struct = image._get_data_struct()
	print(
		json.dumps(data_struct,
					indent=1,
					separators=(',',':')
					),
		)


def main():

	parser = argparse.ArgumentParser()
	parser.add_argument('filename', 
						help="The file that will be parsed as SatoriImage"
						)

	parser.add_argument('--quiet', '-q',
						help=("Does not print a beautified JSON "
						"representation of the SatoriImage"),
						default=False,
						action='store_true',
						)

	args = parser.parse_args()

	satori_pkl = SatoriPickler()
	satori_jsn = SatoriJsoner()
	satori_pkl_uncompress = SatoriPickler(compress=False)
	satori_jsn_uncompress = SatoriJsoner(compress=False)

	image_serializers = [
							satori_pkl,
							satori_jsn,
							satori_pkl_uncompress,
							satori_jsn_uncompress,
						]

	for serializer in image_serializers:
		try:
			image = serializer.read(args.filename)
			if not args.quiet:
				display_image(image)

			print("[+] File is a {compress} {type} SatoriImage"
				.format(
						compress="compressed" if serializer.compress else "",
						type=serializer._type
					),
					file=sys.stderr,
				)
			return
		except Exception as e:
			# print(
			# 	"[!] {}".format(e),
			# 	file=sys.stderr,
			# 	)
			pass
	print ("File '{}' is not of a known SatoriImage format".format(args.filename))


if '__main__' == __name__:
	main()