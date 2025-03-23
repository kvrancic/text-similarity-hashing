import hashlib
import sys

def generate_simhash(text):
    # Tokenize the text
    tokens = text.strip().split()
    # Init the vector with 0 of size 128 due to md5 hash
    vector = [0]*128

    for token in tokens:
        # calculate MD5 hash of the token
        md5_hash = hashlib.md5(token.encode()).hexdigest()
        # Convert the hash to 128 bit binary
        binary_hash = format(int(md5_hash, 16), '0128b')

        for i in range(128):
            if binary_hash[i] == '1':
                vector[i] += 1
            else:
                vector[i] -= 1
    
    simhash_bits = ['1' if v >= 0 else '0' for v in vector]
    
    return format(int(''.join(simhash_bits), 2), '032x')

def hamming_distance(sh1, sh2):
    int1 = int(sh1, 16)
    int2 = int(sh2, 16)
    
    # XOR to find different bits
    xor_result = int1 ^ int2
    
    # Count the number of 1's in the binary representation
    return bin(xor_result).count('1')

def main(): 
    lines = [line.strip() for line in sys.stdin if line.strip()]
    N = int(lines[0])
    texts = lines[1:N+1]

    simhashes = [generate_simhash(text) for text in texts]

    Q = int(lines[N+1])

    for i in range(N+2, N+2+Q):
        query = lines[i].strip().split()
        text_index = int(query[0])
        max_distance = int(query[1])
        
        # Count texts with Hamming distance <= max_distance
        count = -1
        for j in range(N):
            if hamming_distance(simhashes[text_index], simhashes[j]) <= max_distance:
                count += 1
        
        print(count)

if __name__ == '__main__':
    main()