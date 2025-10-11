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
	

def create_dictionary(string):
	# dic = {}                    Alternative implementation kept in case I run into problems
	# for i in string:
	#     if i in dic:
	#         dic[i] += 1
	#     else:
	#         dic[i] = 1
	# return dic
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
		store_codes[node.val]=path
	else:
		encoding(node.left, path + "0", store_codes) #generates the codes, adds 0 for each left node and 1 for each right node
		encoding(node.right, path + "1", store_codes)
	return store_codes


def decoding(root, encoded):
	decoded = []
	cur = root
	for bit in encoded:
		cur = cur.left if bit == "0" else cur.right
		if cur.val is not None:
			decoded.append(cur.val)
			cur = root
	return "".join(decoded)

class Huffman:
	def __init__(self, string):
		self.string=string
		self.dictionary = create_dictionary(string)
		self.que = create_que(self.dictionary)
		self.tree = create_tree(self.que)
		self.codes = encoding(self.tree)

	def root(self):
			return self.tree

	def compress(self):
		return "".join(self.codes[char] for char in self.string)

	def decompress(self, bits):
		return decompress(bits, self.codes)

		
def compress(string, codes):
    return "".join(codes[char] for char in string)

def decompress(bits, codes):
    reversed = {v: k for k, v in codes.items()}
    decoded = []
    current_code = ""

    for bit in bits:
        current_code += bit
        if current_code in reversed:
            decoded.append(reversed[current_code])
            current_code = ""
    return "".join(decoded)



def compress_file(input, output):
    with open(input, "r", encoding="utf-8") as f:
        text = f.read()
    dictionary = create_dictionary(text)
    que = create_que(dictionary)
    tree = create_tree(que)
    codes = encoding(tree)
    bits = compress(text, codes)
    save_compressed(bits, codes, output)


def decompress_file(input, output):
    bits, codes = load_compressed(input)
    text = decompress(bits, codes)
    with open(output, "w", encoding="utf-8") as f:
        f.write(text)


def save_compressed(bits, codes, file): #saves the compressed file
	data = {
		"encoded": bits,
		"codes": codes 
	}
	with open(file, "w", encoding="utf-8") as f:
		json.dump(data, f)


def load_compressed(file): #loads the compressed file
	with open(file, "r", encoding="utf-8") as f:
		data = json.load(f)
	return data["encoded"], data["codes"]