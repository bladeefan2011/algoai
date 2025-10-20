import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))  # gets the correct path
from algoai.huffman.codec import compress_file, decompress_file

def test(input):
	results = os.path.join(os.path.dirname(__file__), "test_results") #creates a folder for the results
	os.makedirs(results, exist_ok=True)

	compressed_file = os.path.join(results, os.path.basename(input) + ".huff") #adds the results to the test_results folder, giving them clear filetypes for which is which
	decompressed_file = os.path.join(results, os.path.basename(input) + ".huff.txt")

	compress_file(input, compressed_file)
	decompress_file(compressed_file, decompressed_file)

	with open(input, "r", encoding="utf-8") as f1: #reads both the original and decompressed files
		original = f1.read()
	with open(decompressed_file, "r", encoding="utf-8") as f2:
		restored = f2.read()

	#Gets all of the filesizes
	original_size = os.path.getsize(input)
	compressed_size = os.path.getsize(compressed_file)
	decompressed_size = os.path.getsize(decompressed_file)

	print(f"File: {os.path.basename(input)}") #lists all the stats
	print(f"Original: {original_size} bytes")
	print(f"Compressed: {compressed_size} bytes")
	print(f"Decompressed:{decompressed_size} bytes")
	print(f"Original and decompressed match: {original == restored}")
	print(f"Ratio: {compressed_size/original_size}")

if __name__ == "__main__":
	#Gets the absolute path to the test_files folder
	test_folder = os.path.join(os.path.dirname(__file__), "..", "test_files")
	test_folder = os.path.abspath(test_folder)

	for file in os.listdir(test_folder): #gets all of the .txt files in the folder and tests them
		if file.endswith(".txt"):
			test(os.path.join(test_folder, file))
