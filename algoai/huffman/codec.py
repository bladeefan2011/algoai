from collections import Counter
import heapq
import json

class Node:
	def __init__(self, freq, val=None, left=None, right=None): 
		self.freq = freq #the frequency of each letter
		self.val = val #the value itself, i.e. symbol
		self.left = left #left node of the tree
		self.right = right # right node of the tree

	def __lt__(self, other):
		return self.freq < other.freq

	def __str__(self):
		if self.val is not None: #making sure the output is in the correct format
			return f"'{self.val}':{self.freq}" 
		else:
			return f"Node({self.freq})"
	
def create_dictionary(string): #creates the dictionary with the frequency of each letter in the string
	return Counter(string)

def create_que(dic): #creates the queue which is then used to create the tree itself in the following function. using heaps is effective
	heap = []
	for val, freq in dic.items():
		node = Node(val=val, freq=freq)
		heap.append(node)
	heapq.heapify(heap)
	return heap

def create_tree(que): #creates the tree itself using the create_que function
	if not que:
		return None
	while len(que) > 1:
		left = heapq.heappop(que)
		right = heapq.heappop(que)
		merged = Node(freq=left.freq + right.freq, val = None, left = left, right = right)
		heapq.heappush(que, merged)
	return que[0]

def encoding(node, path="", store_codes=None): #generating the codes for the algorithm to use in order to decode it
	if store_codes==None:
		store_codes={}
	if node.val is not None:
		store_codes[node.val]=path or "0" #if the string is only a single character
	else:
		encoding(node.left, path + "0", store_codes) #generates the codes, adds 0 for each left node and 1 for each right node
		encoding(node.right, path + "1", store_codes)
	return store_codes

def decoding(root, encoded): #decodes the string from the tree
	decoded = []
	cur = root
	for bit in encoded:
		cur = cur.left if bit == "0" else cur.right #traverses the tree
		if cur.val is not None:
			decoded.append(cur.val)
			cur = root
	return "".join(decoded)

class Huffman:
	def __init__(self, string): #I assume this is clear
		self.string=string
		self.dictionary = create_dictionary(string)
		self.que = create_que(self.dictionary)
		self.tree = create_tree(self.que)
		self.codes = encoding(self.tree)

	def root(self):
			return self.tree

def compress(string, codes): #encodes the string using generated codes
	return "".join(codes[char] for char in string)

def decompress(bits, codes): #decodes the string from the tree
	reversed = {}
	for char, code in codes.items():
		reversed[code] = char #reverses the codes dictionary to make lookup easier
	decoded = []
	current_code = ""

	for bit in bits:
		current_code += bit
		if current_code in reversed:
			decoded.append(reversed[current_code])
			current_code = ""
	return "".join(decoded)

def compress_file(input, output): #compresses the file with input and output paths
	with open(input, "r", encoding="utf-8") as f:
		text = f.read()
	dictionary = create_dictionary(text)
	que = create_que(dictionary)
	tree = create_tree(que)
	codes = encoding(tree)
	bits = compress(text, codes)
	save_compressed(bits, codes, output)

def decompress_file(input, output): #decompresses the file with input and output paths
	bits, codes = load_compressed(input)
	text = decompress(bits, codes)
	with open(output, "w", encoding="utf-8") as f:
		f.write(text)

def save_compressed(bits, codes, file): #saves the compressed file with the metadata needed for decompression
	bytear = bytearray()
	for i in range(0, len(bits), 8):
		byte = bits[i:i+8] #gets 8 bits each time
		bytear.append(int(byte.ljust(8, "0"), 2)) #adds extra 0s to the end if last byte is incomplete

	metadata = {
		"codes": codes,
		"bit_length": len(bits)}

	with open(file, "wb") as f:
		metadata_bytes = json.dumps(metadata, separators=(",", ":")).encode("utf-8") #converts metadata to json and then to bytes
		f.write(len(metadata_bytes).to_bytes(4, "big"))
		f.write(metadata_bytes)
		f.write(bytear)

def load_compressed(file): #loads the compressed file and gets everything needed for decompression
	with open(file, "rb") as f:
		meta_len = int.from_bytes(f.read(4), "big")
		metadata = json.loads(f.read(meta_len).decode("utf-8"))
		compressed = f.read()

	bit_len = len(compressed)*8
	int_val = int.from_bytes(compressed, byteorder="big") #converts bytes to integer
	bits = bin(int_val)[2:] #converts integer to bits
	bits = bits.zfill(bit_len) #adds leading zeros back
	bits = bits[:metadata["bit_length"]]
	return bits, metadata["codes"]