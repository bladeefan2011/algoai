def read_file(file):
    with open (file, r) as f:
        data = f.read()
    return data


def write_file(file, compression):
    with open (file, w) as f:
        f.write(compression)
    