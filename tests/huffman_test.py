import os
import tempfile
import unittest
from algoai.huffman.codec import (compress_file, decompress_file, create_dictionary, create_tree, encoding, decoding, Huffman,)

class TestHuffmanCodec(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.tmpdir = self.tmp.name

    def tearDown(self):
        self.tmp.cleanup()

    def _write_file(self, name, content):
        path = os.path.join(self.tmpdir, name)
        with open(path, "w", encoding="utf-8") as file:
            file.write(content)
        return path

    def test_roundtrip_file(self):
        content = "fortnite_is_awesome"
        input = self._write_file("input.txt", content)
        compr = os.path.join(self.tmpdir, "compressed.huff")
        output = os.path.join(self.tmpdir, "output.txt")

        compress_file(input, compr)
        decompress_file(compr, output)

        with open(output, encoding="utf-8") as file:
            result = file.read()
        self.assertEqual(result, content)

    def test_dictionary_and_tree(self):
        s = "aaabbc"
        d = create_dictionary(s)
        self.assertEqual(d["a"], 3)
        self.assertEqual(d["b"], 2)
        self.assertEqual(d["c"], 1)

        q = list(d.items())
        self.assertTrue(q)
        tree = create_tree([])
        self.assertIsNone(tree) 

    def test_encoding_and_decoding(self):
        text = "fortnite_is_awesome"
        huff = Huffman(text)
        bits = "".join(huff.codes[char] for char in text)
        decoded = decoding(huff.tree, bits)
        self.assertEqual(decoded, text)

    def test_nonexistent_file(self):
        fake_test = os.path.join(self.tmpdir, "not_real.txt")
        fake_result = os.path.join(self.tmpdir, "out.txt")
        with self.assertRaises(FileNotFoundError):
            compress_file(fake_test, fake_result)

if __name__ == "__main__":
    unittest.main()
