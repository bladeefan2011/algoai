import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))  # gets the correct path
from algoai.lz78.codec import compress_file, decompress_file

def test(input):
    compressed_file = input + ".lz78"
    decompressed_file = input + ".lz78.txt"

    compress_file(input, compressed_file)
    decompress_file(compressed_file, decompressed_file)

    with open(input, "r", encoding="utf-8") as file1, \
         open(decompressed_file, "r", encoding="utf-8") as file2:
        original = file1.read()
        restored = file2.read()

    #Gets all of the filesizes
    original_size = os.path.getsize(input)
    compressed_size = os.path.getsize(compressed_file)
    decompressed_size = os.path.getsize(decompressed_file)

    print(f"File: {os.path.basename(input)}")
    print(f"Original: {original_size} bytes")
    print(f"Compressed: {compressed_size} bytes")
    print(f"Decompressed:{decompressed_size} bytes")
    print(f"Original and decompressed match: {original == restored}")
    print(f"Ratio: {compressed_size/original_size}")

if __name__ == "__main__":
    #Gets the absolute path to the test_files folder
    test_folder = os.path.join(os.path.dirname(__file__), "..", "test_files")
    test_folder = os.path.abspath(test_folder)

    files = [file for file in os.listdir(test_folder) if file.endswith(".txt")]
    for filename in files:
        test(os.path.join(test_folder, filename))
