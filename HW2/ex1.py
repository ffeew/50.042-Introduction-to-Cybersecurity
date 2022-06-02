# Completed by Koh Aik Hong 1005139
import matplotlib.pyplot as plt

def decrypt(text, cipher, substitute):
    output = ""
    for letter in text:
        if letter in cipher.upper():
            index = cipher.upper().index(letter)
            output += substitute[index].upper()
        else:
            output += letter
    return output

fin = open("story_cipher.txt", mode="r", encoding="utf-8", newline="\n")
text = fin.read()

decrypted_text_v9 = decrypt(text, "ujyqdixhtwmelvsorbanfckzp", "etianshrdgwovfcyblkxpmujz")

fout = open("solution.txt", mode="w", encoding="utf-8", newline="\n")
fout.write(decrypted_text_v9)