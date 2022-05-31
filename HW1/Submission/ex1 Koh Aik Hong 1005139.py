#!/usr/bin/env python3
# SUTD 50.042 FCS Lab 1
# Simple file read in/out
# Completed by: Koh Aik Hong, 1005139


# Import libraries
import sys
import argparse
import string


def doStuff(filein, fileout):
    # open file handles to both files
    fin = open(filein, mode="r", encoding="utf-8", newline="\n")  # read mode
    fin_b = open(filein, mode="rb")  # binary read mode
    fout = open(fileout, mode="w", encoding="utf-8", newline="\n")  # write mode
    fout_b = open(fileout, mode="wb")  # binary write mode
    c = fin.read()  # read in file into c as a str
    # and write to fileout

    # close all file streams
    # fin.close()
    # fin_b.close()
    # fout.close()
    # fout_b.close()

    # PROTIP: pythonic way
    with open(filein, mode="r", encoding="utf-8", newline="\n") as fin:
        text = fin.read()
        # do stuff
        alphabet = [char for char in string.printable]
        k = args.key
        m = args.mode.lower()
        # len(string.printable = 100)
        result = ""
        if  not (k>0 and k<len(string.printable)):
            print(f"key is out of valid range. Key must be between 0 and {len(string.printable)-1}")
            return
        if m == "d":
            # subtract from the unicode value
            for char in text:
                shifted_index = (alphabet.index(char) - k + 100) % 100
                result += alphabet[shifted_index]
            fout.write(result)
            return
        
        elif m == "e":
            #add to unicode value
            for char in text:
                shifted_index = (alphabet.index(char) + k) % 100
                result += alphabet[shifted_index]
            fout.write(result)
            return
        

        # file will be closed automatically when interpreter reaches end of the block


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
