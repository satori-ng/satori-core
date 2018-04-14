import argparse
import json

from satoricore.serialize.pickle import SatoriPickler


parser = argparse.ArgumentParser()
parser.add_argument('filename', 
					help="The file that will be parsed as SatoriImage"
					)

parser.add_argument('--type', '-t',
					help="The type of serialization of the file",
					default=None
					)
args = parser.parse_args()

pkl = SatoriPickler()
try:
	image = pkl.read(args.filename)
	print("[+] File is a compressed Pickle SatoriImage")
except Exception as e:
	print(e)





data_struct = image._get_data_struct()

print(
	json.dumps(data_struct,
				indent=1,
				separators=(',',':')
				)
	)