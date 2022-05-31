fin_b = open("sherlock.txt", mode="rb")  # binary read mode

with open("sherlock.txt", mode="rb") as fin:
    s = fin.read(1)
    mybytearr = bytearray()
    while s:
        mybytearr += s
        s = fin.read(1)
    mybytearr += s

    # for i in range(len(mybytearr)):
    #     byte = mybytearr[i]
    #     mybytearr[i] = mybytearr[i] +1
    #     print(byte)

    print(mybytearr)
    # text = fin_b.read(1)
    # x = (146).to_bytes(2,byteorder='big')
    # print(x)
    # print(text)
    # print(sum(text,x))
