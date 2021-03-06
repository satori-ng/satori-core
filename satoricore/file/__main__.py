import argparse
import json
import sys

from satoricore.file.pickle import SatoriPickler
from satoricore.file.json import SatoriJsoner
from satoricore.logger import logger, set_debug_logger


def display_image(image):
	data_struct = image._get_data_struct()
	print(
		json.dumps(
				data_struct,
				indent=1,
				separators=(',',':'),
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

	parser.add_argument('--debug', '-d',
						help=("Enables debug logging"),
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

	if args.debug : set_debug_logger()

	for serializer in image_serializers:
		try:
			image = serializer.read(args.filename)
			if not args.quiet:
				display_image(image)

			logger.info("File is a {compress} {type} SatoriImage"
				.format(
						compress="compressed" if serializer.compress else "",
						type=serializer._type
					),
				)
			return True

		except FileNotFoundError as fe:
			logger.critical("File '{}' not found".format(args.filename))
			sys.exit(-2)

		except Exception as e:
			logger.debug("{} - {}".format(serializer, e))

	logger.error("File '{}' is not of a known SatoriImage format"
		.format(
				args.filename,
			)
		)


if '__main__' == __name__:
	main()