def encoding(string): #encodes the string in to a dictionary
    if not string:
        return []
    dic = {}
    current =""
    dic_size = 1
    encoded = []

    for char in string:
        new_char = current + char
        if new_char in dic:
            current = new_char
        else: 
            if current == "":
                encoded.append((0, char))
            else:
                encoded.append((dic[current], char))
            dic[new_char] = dic_size
            dic_size += 1
            current = ""
    
    if current != "":
        encoded.append((dic[current], ""))  
    return encoded


def decoding(dictionary): #decodes the dictionary back to a string
    dec_dic = {0: ""}
    result = []
    dic_size = 1

    for index, char in dictionary:
        entry = dec_dic[index] + char
        result.append(entry)
        dec_dic[dic_size] = entry
        dic_size += 1

    return "".join(result)



text = "89214ku1489kuadk19eju9i1d2ujio18am79dmjm81diajkop0dj189dqk7uja98duhj1md8u9jad1798mdja8udhj1789maydhnm12,6785y1hm,9i9ad.akoldpapdppöadakd819udjk1qd7891dyham,87d621hydm1"
result = encoding(text)
decoded = decoding(result)

print(result)
print(decoded)

print (text == decoded)