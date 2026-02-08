# AlgoAI

This repository contains the coursework for the course **"Algoritmit ja tekoäly"**.

---

## Setup Instructions

Follow these steps to get the project running on your local machine.

### 1. Clone the repository

```bash
git clone git@github.com:bladeefan2011/algoai.git
```

### 2. Change into the project directory

```bash
cd algoai
```

### 3. Install dependencies

```bash
poetry install --with dev
```

### 4. Activate the Poetry shell

```bash
poetry shell
```

### Running Tests

### 5. Run individual tests

```bash
pytest -v
```

### 6. Run compression tests

```bash
python tests/huffman_test_compression.py
```
```bash
python tests/lz78_test_compression.py
```

### Test coverage

### 7. Run coverage

```bash
coverage run -m pytest
```
### 8. Print coverage report

```bash
coverage report -m
```
