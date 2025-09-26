import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from lz78.codec import compress_file, decompress_file

def test(folder="test_files"):  #tests the entire folder, be careful
    for file in os.listdir(folder):
        if file.endswith(".txt"):
            path = os.path.join(folder, file)
            comp_path = path + ".lz78"
            out_path = path + ".out.txt"

            compress_file(path, comp_path)
            decompress_file(comp_path, out_path)

            with open(path, "r", encoding="utf-8") as f1, open(out_path, "r", encoding="utf-8") as f2:
                original, new = f1.read(), f2.read()

            print(original == new)

if __name__ == "__main__":
    test()
