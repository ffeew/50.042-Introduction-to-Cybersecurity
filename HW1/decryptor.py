# def doStuff(filein, fileout):
#     # open file handles to both files
#     fin_b = open(filein, mode="rb")  # binary read mode


#     # PROTIP: pythonic way
#     with open(filein, mode="rb") as fin_b:
#         # do stuff
#         s = fin_b.read(1)
#         mybytearr = bytearray()
#         # while s:
#         #     mybytearr += s
#         #     s = fin_b.read(1)

#         # k = 253

#         # for i in range(len(mybytearr)):
#         #     mybytearr[i] = (mybytearr[i] - k + 255) % 255
#         # fout_b.write(mybytearr)
#         # return

#         i = 0
#         while i<60:
#             mybytearr += s
#             s = fin_b.read(1)
#             i+=1

#         for k in range(256):
#             newbytearr = mybytearr[:]
#             for i in range(len(mybytearr)):
#                 newbytearr[i] = (newbytearr[i] - k + 256) % 256
#             fout_b = open(f"./pics/answer{k}.png", mode="wb")  # binary write mode
#             fout_b.write(newbytearr)
#             print(newbytearr)
# doStuff("flag", "answer.png")

import sys
import argparse

def readFlag(flag):
	try:
		byte=open(flag, mode='rb').read()
	except FileNotFoundError:
		print('Can\'t find the input file.')
	return byte

def shiftCipher(inbyte,fileout,key):
	outbyte=bytearray()
	for i in inbyte:
		outbyte.append((i+256-key)%256)

	fout=open(fileout, mode='wb')
	fout.write(outbyte)
	return True

def decryptFlag(flag):
	flagbytes=readFlag(flag)
	for key in range (1, 256):
		name='./pics/answer'+str(key)
		shiftCipher(flagbytes,name,key)



if __name__=="__main__":
	parser=argparse.ArgumentParser()
	parser.add_argument('flag')
	args=parser.parse_args()
	flag=args.flag

	decryptFlag(flag)