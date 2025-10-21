import struct
from bitarray import bitarray

def encoding(string): #encodes the data
	if not string:
		return []
	dic = {}
	current = "" #holds the current substring, empty at start
	dic_size = 1
	encoded = [] #list holds the encoded tuples

	for char in string:
		new_char = current + char
		if new_char in dic: #if the new substring is in the dict, update current
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


def decoding(dictionary): #decodes the data
	dec_dic = {0: ""}
	result = []
	dic_size = 1 #init the dict size

	for index, char in dictionary: #iterating the dictionary
		entry = dec_dic[index] + char
		result.append(entry)
		dec_dic[dic_size] = entry #adding new entry to the dict
		dic_size += 1

	return "".join(result)


def save_compressed(filename, encoded):
	if not encoded:
		return
	
	max_index = max(index for index, j in encoded)
	chars = []
	for i, char in encoded:
		if char:
			chars.append(char)
	max_char = max((ord(char) for char in chars), default=0)

	index_bits = max(8, max_index.bit_length() or 1)
	char_bits = max(8, max_char.bit_length() or 1)

	with open(filename, "wb") as f:
		f.write(struct.pack("BB", index_bits, char_bits))

		bits = bitarray(endian="big")
		for index, char in encoded:
			index_binary = bin(index)[2:].zfill(index_bits) #convert index to binary
			if char:
				char_val = ord(char)
			else:
				char_val = 0
			char_binary = bin(char_val)[2:].zfill(char_bits) #convert char to binary
			bits.extend(index_binary + char_binary) #adds index and char binary to bitarray

		bits.tofile(f) #writes bitarray to file


def load_compressed(filename):
	encoded = []
	with open(filename, "rb") as f:
		header = f.read(2) #reads the first 2 bytes
		if len(header) < 2: #file is empty
			return []
		index_bits, char_bits = struct.unpack("BB", header)

		bits = bitarray(endian="big")
		bits.fromfile(f)
		bitstring = bits.to01() #converts bitarray to string of bits

		total_bits = index_bits + char_bits #total bits in tuple
		length = len(bitstring) // total_bits * total_bits #removes the padding
		bitstring = bitstring[:length]

		for i in range(0, length, total_bits):
			id_str = bitstring[i : i + index_bits] #index bits
			ch_str = bitstring[i + index_bits : i + total_bits] #char bits  
			index = int(id_str, 2) 
			char_val = int(ch_str, 2)
			if char_val != 0:
				char = chr(char_val)
			else:
				char = ""
			encoded.append((index, char))

	return encoded


def compress_file(input_file, output_file): #compresses the file
	with open(input_file, "r", encoding="utf-8") as f:
		text = f.read()
	encoded = encoding(text)
	save_compressed(output_file, encoded)


def decompress_file(input_file, output_file): #decompresses the file
	encoded = load_compressed(input_file)
	decoded = decoding(encoded)
	with open(output_file, "w", encoding="utf-8") as f:
		f.write(decoded)
