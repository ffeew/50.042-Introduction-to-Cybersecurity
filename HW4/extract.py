#!/usr/bin/env python3
# ECB plaintext extraction skeleton file for 50.042 FCS

import argparse
from collections import Counter

def getInfo(headerfile):
    with open(headerfile, "rb") as fin:
        info = fin.read()
    return info

def extract(infile, outfile, headerfile):
    info = getInfo(headerfile)

    blocks = []

    # with open(infile, "rb") as fin:
    #     data = fin.read()
    #     data_length = len(data)
    #     print(data_length)
    #     bytes_per_pixel = (data_length - len(info) - 1)/(480*640)
    #     print(bytes_per_pixel)

    # assuming file is encrypted with block encryption, block size = 8 bytes
    # block size = 4 works as well, but there will be stripes in the decrypted image
    # block size = 2 works as well, but there will be stripes in the decrypted image and the pattern is less discernible
    # block size = 1 works as well, but there will be stripes in the decrypted image and the pattern is even less discernible

    with open(infile, "rb") as fin:
        fin.read(len(info) + 1)
        block = fin.read(8)
        while block:
            blocks.append(block)
            block = fin.read(8)

    block_frequency = Counter(blocks)

    most_frequent_block = block_frequency.most_common(1)[0][0]

    # aim: replace the most frequently occuring patterns with 8 1s, the others replace them with 0s
    out = [b"1" * 8 if block == most_frequent_block else b"0" * 8 for block in blocks]

    out = "".join([block.decode() for block in out]).encode()

    with open(outfile, "wb") as fout:
        fout.write(info + b"\n" + out)

if __name__=="__main__":
    parser=argparse.ArgumentParser(description='Extract PBM pattern.')
    parser.add_argument('-i', dest='infile',help='input file, PBM encrypted format')
    parser.add_argument('-o', dest='outfile',help='output PBM file')
    parser.add_argument('-hh', dest='headerfile',help='known header file')

    args=parser.parse_args()
    infile=args.infile
    outfile=args.outfile
    headerfile=args.headerfile

    print('Reading from: %s'%infile)
    print('Reading header file from: %s'%headerfile)
    print('Writing to: %s'%outfile)

    success=extract(infile,outfile,headerfile)

    # python extract.py -i letter.e -o decrypted_letter.pbm -hh header.pbm   