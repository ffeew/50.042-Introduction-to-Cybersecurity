import pandas as pd

def hashcat_output_to_csv(filehandlers):
    output = []
    for filehandler in filehandlers:
        for line in filehandler:
            hash_plaintext = line.split(":")
            output.append([x.strip() for x in hash_plaintext])
    return output

file1 = open("cracked_passwords_append.txt", mode = "r")
file2 = open("cracked_passwords_prepend.txt", mode = "r")
file3 = open("crackedpasswords_bruteforce.txt", mode = "r")

header = ["md5 hash", "plaintext"]
data = hashcat_output_to_csv([file1, file2, file3])
data = pd.DataFrame(data, columns=header)
data.to_csv('ex5.csv', index=False)