#!/usr/bin/env python3
# SUTD 50.042 FCS Lab 1
# Simple file read in/out
# Completed by Koh Aik Hong, 1005139

# Import libraries
import sys
import argparse
import string


def doStuff(filein, fileout):
    # open file handles to both files
    fout_b = open(fileout, mode="wb")  # binary write mode

    k = args.key
    m = args.mode.lower()

    # PROTIP: pythonic way
    with open(filein, mode="rb") as fin_b:
        # do stuff
        mybytearr = generate_byte_array(fin_b)
        new_byte_arr = bytearray()

        if  not (k>0 and k<256):
            print(f"key is out of valid range. Key must be between 0 and 255")
            return

        if m == "d":
            # subtract from the unicode value
            for i in range(len(mybytearr)):
                new_byte_arr.append((mybytearr[i] - k + 256) % 256)
            fout_b.write(new_byte_arr)
            return
        
        elif m == "e":
            #add to unicode value
            for i in range(len(mybytearr)):
                new_byte_arr.append((mybytearr[i] + k + 256) % 256)
            fout_b.write(new_byte_arr)
            return
        

        # file will be closed automatically when interpreter reaches end of the block

def generate_byte_array(file_handler):
    byte_arr = file_handler.read()
    return byte_arr


# our main function
if __name__ == "__main__":
    # set up the argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", dest="filein", help="input file")
    parser.add_argument("-o", dest="fileout", help="output file")
    parser.add_argument("-k", "--key", dest = "key", type=int, help="encryption key")
    parser.add_argument("-m", "--mode", dest = "mode", help="encryption or decryption mode")
    # parse our arguments
    args = parser.parse_args()
    filein = args.filein
    fileout = args.fileout

    doStuff(filein, fileout)

    # all done
