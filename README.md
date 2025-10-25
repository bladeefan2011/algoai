# algoai
The coursework for the course "Algoritmit ja tekoäly"

1. Clone the repository
>git clone https://github.com/bladeefan2011/algoai.git
2. Change to the directory
>cd algoai
1. Install dependencies
>poetry install --with dev
4. Initialize shell
>poetry shell
5. Run individual tests
>pytest -v
6. Or alternatively run the compression tests
>python tests/huffman_test_compression.py
>python tests/lz78_test_compression.py
7. Check test coverage
>coverage run -m pytest
 coverage report -m
