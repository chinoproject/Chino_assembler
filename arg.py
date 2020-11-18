import argparse

output_hex = True
input_filename = ""
output_filename = "a.txt"


parser = argparse.ArgumentParser(description='ChinoCPU编译器')
parser.add_argument("input_filename")
parser.add_argument("-o","--output",type=str)
parser.add_argument("-b","--binary",action="store_true")
args = parser.parse_args()

output_filename = args.output
input_filename = args.input_filename
output_hex = not args.binary