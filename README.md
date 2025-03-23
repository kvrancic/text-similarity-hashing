# SimHash-Based Text Similarity Detection

This repository contains the implementation of two approaches for detecting similar texts using the SimHash algorithm. The project was developed as part of a data analysis course at FER (University of Zagreb), focused on identifying near-duplicate documents through hashing techniques.

## 📌 Overview

SimHash is a locality-sensitive hashing algorithm that maps similar documents to similar hash values, enabling fast and memory-efficient comparison of texts. This project includes two main tasks:

### Task A - Sequential Similarity Search
- Compute 128-bit SimHash for each input text using `md5` hashing of tokenized words.
- For each query, determine how many documents differ from the given one by at most `K` bits (Hamming distance).
- Brute-force comparison with all hashes.

### Task B - Optimized Search with Locality Sensitive Hashing (LSH)
- Use SimHash to generate 128-bit signatures for all documents.
- Apply LSH to split the hash into `b=8` bands of `r=16` bits each.
- Only compare documents that share at least one identical band (bucket) with the target.
- Greatly improves scalability to 100,000+ documents.

## 🧪 Input Format

Input file format (for both A and B):

```
N
text_0
...
text_N-1
Q
I_0 K_0
...
I_Q-1 K_Q-1
```

Where:
- `N`: number of documents
- `Q`: number of queries
- Each query compares the `I`-th document against all others, counting how many differ by at most `K` bits.

## 🚀 How to Run

### Python

#### Task A
```bash
python SimHash.py < input.txt > output.txt
```

#### Task B
```bash
python SimHashBuckets.py < input.txt > output.txt
```

## 🛠 Implementation Notes

- Hashing: `md5` is used as a base hash function.
- Language: Python 3.
- Libraries used: Only built-in libraries like `hashlib`, `collections`, etc.
- Time Constraints:
  - Task A: ≤ 20 seconds
  - Task B: ≤ 200 seconds (for Python)

## 📁 File Structure

```
.
├── SimHash.py              # Task A implementation
├── SimHashBuckets.py       # Task B implementation using LSH
├── README.md
```

## 📚 References

- [SimHash Paper (Google)](https://www.fer.unizg.hr/_download/repository/AVSP_01_Near_Duplicates_Simhash.pdf)
- [Locality Sensitive Hashing (LSH)](https://www.fer.unizg.hr/_download/repository/AVSP_02_Finding_Similar_Items.pdf)

## 👨‍🎓 Author

Developed by Karlo Vrančić as part of the **Big Data Analysis (AVSP)** course at the **University of Zagreb - FER**.