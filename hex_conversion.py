#!/usr/bin/python

import sys


def main():
	if len(sys.argv[1:]) != 2:
		print "hex_conversion: Convert to hex, Ascii or decimal."
		print "\nUsage: ./hex_conversion <string> <-2hex/-2ascii/-2dec>"
		print "Example: ./hex_conversion 41 -2ascii\n"
		sys.exit(0)

	# Original input
	to_convert = sys.argv[1]
	mode = sys.argv[2]

	# Conversion
	if mode == '-2hex':
		in_hex = '0x' + to_convert.encode('hex')
		print 'Original:', to_convert, '\nHex:', in_hex
	elif mode == '-2ascii':
		in_ascii = to_convert.decode('hex')
		print 'Original:', to_convert, '\nAscii:', in_ascii
	elif mode == '-2dec':
		in_dec = int(to_convert, 16)
		print 'Original:', to_convert, '\nDecimal:', in_dec
	else:
		print 'Improper format. Review and re-submit.\n'
		sys.exit(0)


main()
	
