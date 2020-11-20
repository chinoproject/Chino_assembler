import argparse


output_hex = True
input_filename = "test.asm"
output_filename = "a.txt"
rtl_code_gen = True

parser = argparse.ArgumentParser(description='ChinoCPU编译器')
parser.add_argument("input_filename")
parser.add_argument("-o","--output",type=str)
parser.add_argument("-b","--binary",action="store_true")
parser.add_argument("-r","--close-rtl-gen",action="store_true")

args = parser.parse_args()
if args.output != None:
    output_filename = args.output
input_filename = args.input_filename
output_hex = not args.binary
rtl_code_gen = not args.close_rtl_gen