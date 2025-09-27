import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))) #gets the correct path
from huffman.codec import compress_file, decompress_file


def test(input): #tests the flle by compressing it and decompressing it and then comparing the original file and the decompressed file
    compressed_file = input + ".huff"
    decompressed_file = input + ".out.txt"
    compress_file(input, compressed_file)
    decompress_file(compressed_file, decompressed_file)
    with open(input, "r", encoding="utf-8") as file1, \
         open(decompressed_file, "r", encoding="utf-8") as file2:
        original = file1.read()
        restored = file2.read()

    print(original == restored)
    
if __name__ == "__main__":
    test_folder = "test_files"
    files = [file for file in os.listdir(test_folder) if file.endswith(".txt")]
    for filename in files:
        test(os.path.join(test_folder, filename))

