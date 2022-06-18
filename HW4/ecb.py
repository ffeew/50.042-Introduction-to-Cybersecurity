#!/usr/bin/env python3
# ECB wrapper skeleton file for 50.042 FCS

from present import *
import argparse
import secrets
from cryptography.hazmat.primitives import padding

nokeybits=80
blocksize=64 # 64 bits block length = 8 bytes

def pad(block):
    padding_length = 8-len(block)%8
    return block + bytes([padding_length])*padding_length

def unpad(cipher):
    return cipher[:-cipher[-1]]

def ecb(infile,outfile,keyfile,mode):
    with open(keyfile, "rb") as fin:
        key = int.from_bytes(fin.read(), byteorder='big')

    fin = open(infile, mode="rb")
    fout = open(outfile, mode="wb")

    if mode.lower() == "e":
        print("Encrypting now......")
        
        block = fin.read(8)
        while block:
            padded_block = pad(block)
            for i in range(len(padded_block)//8):
                subBlock = int.from_bytes(padded_block[i*8 : (i+1)*8], "big")
                encrypted_subBlock = present(subBlock, key).to_bytes(8, "big")
                fout.write(encrypted_subBlock)
            block = fin.read(8)

    elif mode.lower() == "d":
        print("Decrypting now......")
        # 16 bytes result after PKCS#7 padding
        block = fin.read(8*2)
        while block:
            # out = b''
            for i in range(len(block)//8):
                subBlock = int.from_bytes(block[i*8 : (i+1)*8], "big")
                decrypted_subBlock = present_inv(subBlock, key)
                out+=decrypted_subBlock.to_bytes(8, "big")
            unpadded_block = unpad(bytes(out))
            fout.write(unpadded_block)
            block = fin.read(8*2)

    fin.close()
    fout.close()

if __name__=="__main__":
    parser=argparse.ArgumentParser(description='Block cipher using ECB mode.')
    parser.add_argument('-i', dest='infile',help='input file')
    parser.add_argument('-o', dest='outfile',help='output file')
    parser.add_argument('-k', dest='keyfile',help='key file')
    parser.add_argument('-m', dest='mode',help='mode')

    args=parser.parse_args()
    infile=args.infile
    outfile=args.outfile
    keyfile=args.keyfile
    mode = args.mode

    ecb(infile, outfile, keyfile, mode)

# python ecb.py -i Tux.pbm -o encrypted_Tux.pbm -k keyfile -m e 
# python ecb.py -i encrypted_Tux.pbm -o decrypted_Tux.pbm -k keyfile -m d