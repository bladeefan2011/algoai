import os
import sys
import algoai.huffman.codec as huffman_codec
import algoai.lz78.codec as lz78_codec

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
file_dir = os.path.join(os.path.dirname(__file__), "..", "test_files")

def get_filesize(data_or_bytes):
    if isinstance(data_or_bytes, str):
        if set(data_or_bytes) <= {"0", "1"} and len(data_or_bytes) > 8:
            return len(data_or_bytes) / 8
        else:
            return len(data_or_bytes.encode("utf-8"))
    elif isinstance(data_or_bytes, bytes):
        return len(data_or_bytes)
    elif isinstance(data_or_bytes, list):
        import json
        return len(json.dumps(data_or_bytes).encode("utf-8"))
    else:
        return len(str(data_or_bytes).encode("utf-8"))

def choose_algorithm():
    while True:
        print("Choose compression algorithm:")
        print("1. Huffman")
        print("2. LZ78")
        choice = input("Enter 1 or 2: ").strip()
        if choice == "1":
            return "huffman"
        elif choice == "2":
            return "lz78"
        else:
            print("Invalid algorithm.")
    
def choose_mode():
    while True:
        print("Do you want to:")
        print("1. Compress a string")
        print("2. Compress a file from test_files/")
        choice = input("Enter 1 or 2: ").strip()
        if choice in ("1", "2"):
            return choice
        else:
            print("Invalid mode.")
        

def compress_string(data, algo):
    if algo == "huffman":
        huff = huffman_codec.Huffman(data)
        codes = huff.codes
        return huffman_codec.compress(data, codes)
    elif algo == "lz78":
        return lz78_codec.encoding(data)
    else:
        raise ValueError()

def main():
    print("Welcome!")
    print("Data Compression Test")
    algo = choose_algorithm()
    mode = choose_mode()

    if mode == "1":
        data = input("Enter the string to compress: ")
        compressed = compress_string(data, algo)

        original_size = get_filesize(data)
        compressed_size = get_filesize(compressed)
        ratio = (compressed_size / original_size) * 100 if original_size > 0 else 0

        print("Compression Results")
        print(f"Algorithm: {algo}")
        print(f"Original size: {original_size} bytes")
        print(f"Compressed size: {compressed_size} bytes")
        print(f"Compress ratio: {ratio}%")

    else:
        files = [f for f in os.listdir(file_dir) if f.endswith(".txt")]
        if not files:
            print("No correct files found in test_files")
            return

        print("Available test files:")
        for i, f in enumerate(files, start=1):
            print(f"{i}. {f}")
        choice = int(input("Select a file by number: ").strip())
        if not (1 <= choice <= len(files)):
            print("Invalid number.")
            sys.exit(1)

        filename = files[choice - 1]
        input_path = os.path.join(file_dir, filename)
        output_path = os.path.join(file_dir, f"{filename}.{algo}.compressed")

        if algo == "huffman":
            huffman_codec.compress_file(input_path, output_path)
        else:
            lz78_codec.compress_file(input_path, output_path)

        original_size = os.path.getsize(input_path)
        compressed_size = os.path.getsize(output_path)
        if original_size > 0:
            ratio = (compressed_size / original_size) * 100
        else:
            ratio = 0

        print("Results")
        print(f"Algorithm: {algo}")
        print(f"Original file: {filename}")
        print(f"Original size: {original_size} bytes")
        print(f"Compressed size: {compressed_size} bytes")
        print(f"Compress ratio: {ratio}%")
        print(f"Saved compressed file as: {output_path}")

if __name__ == "__main__":
    main()
