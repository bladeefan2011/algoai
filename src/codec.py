import struct

def encoding(string):
    if not string:
        return []
    dic = {}
    current = ""
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


def decoding(dictionary):
    dec_dic = {0: ""}
    result = []
    dic_size = 1

    for index, char in dictionary:
        entry = dec_dic[index] + char
        result.append(entry)
        dec_dic[dic_size] = entry
        dic_size += 1

    return "".join(result)


def save_compressed(filename, encoded):
    with open(filename, "wb") as f:
        for index, char in encoded:
            f.write(struct.pack(">HB", index, ord(char) if char else 0))


def load_compressed(filename):
    encoded = []
    with open(filename, "rb") as f:
        while chunk := f.read(3):
            index, char_val = struct.unpack(">HB", chunk)
            char = chr(char_val) if char_val != 0 else ""
            encoded.append((index, char))
    return encoded


def compress_file(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as f:
        text = f.read()
    encoded = encoding(text)
    save_compressed(output_file, encoded)


def decompress_file(input_file, output_file):
    encoded = load_compressed(input_file)
    decoded = decoding(encoded)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(decoded)
