import os
import tempfile
import unittest
from algoai.lz78.codec import (encoding, decoding, compress_file, decompress_file, save_compressed, load_compressed)

class TestLZ78Codec(unittest.TestCase):
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
        content = "abra_kadabra_alakazam"
        input = self._write_file("input.txt", content)
        compr = os.path.join(self.tmpdir, "compressed.lz78")
        output = os.path.join(self.tmpdir, "out.txt")

        compress_file(input, compr)
        decompress_file(compr, output)

        with open(output, encoding="utf-8") as file:
            result = file.read()
        self.assertEqual(result, content)

    def test_encoding_and_decoding_match(self):
        text = "fortnite_is_awesome"
        encoded = encoding(text)
        decoded = decoding(encoded)
        self.assertEqual(decoded, text)

    def test_save_and_load_compressed(self):
        data = encoding("fortnite_is_awesome")
        path = os.path.join(self.tmpdir, "encoded.bin")
        save_compressed(path, data)
        loaded = load_compressed(path)
        self.assertEqual(loaded, data)

    def test_nonexistent_file(self):
        fake_test = os.path.join(self.tmpdir, "not_real.txt")
        fake_result = os.path.join(self.tmpdir, "out.lz78")
        with self.assertRaises(FileNotFoundError):
            compress_file(fake_test, fake_result)

if __name__ == "__main__":
    unittest.main()
