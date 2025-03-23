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
    
    # Create binary representation
    simhash_bits = ['1' if v >= 0 else '0' for v in vector]
    
    # Return as binary string
    return ''.join(simhash_bits)

def hamming_distance(sh1, sh2):
    int1 = int(sh1, 2)
    int2 = int(sh2, 2)
    
    # XOR to find different bits
    xor_result = int1 ^ int2
    
    # Count the number of 1's in the binary representation
    return bin(xor_result).count('1')


def build_lsh(simhashes):
    N = len(simhashes)
    b = 8  # Number of bands
    r = 16  # Bits per band

    candidates = {}  # text_id -> set of candidate text_ids

    # Process each band
    for band in range(b):
        buckets = {}  # Map to store texts that hash to the same bucket
        
        for text_id, sh in enumerate(simhashes):
            # Extract the current band (16 bits)
            band_start = band * r
            band_end = band_start + r
            band_bits = sh[band_start:band_end]
            
            # Convert band bits to an integer to use as bucket key
            band_value = int(band_bits, 2)
            
            # Add to corresponding bucket
            if band_value not in buckets:
                buckets[band_value] = []
            
            # Add current text to the bucket
            buckets[band_value].append(text_id)
            
        # After all texts are processed for this band, identify candidates
        for bucket_values in buckets.values():
            if len(bucket_values) > 1:
                for i in range(len(bucket_values)):
                    text_id = bucket_values[i]
                    if text_id not in candidates:
                        candidates[text_id] = set()
                    
                    # Add all other texts in this bucket as candidates
                    for j in range(len(bucket_values)):
                        if i != j:
                            candidates[text_id].add(bucket_values[j])

    return candidates

def main():
    lines = [line.strip() for line in sys.stdin if line.strip()]

    N = int(lines[0])
    texts = lines[1:N+1]

    simhashes = [generate_simhash(text) for text in texts]
    
    # Build LSH index to find candidate pairs
    candidates = build_lsh(simhashes)

    Q = int(lines[N+1])

    for i in range(N+2, N+2+Q):
        query = lines[i].strip().split()
        text_index = int(query[0])
        max_distance = int(query[1])

        sh_main = simhashes[text_index]
        similar_count = 0

        # Get all candidate texts that could be similar
        to_check = candidates.get(text_index, set())
        
        
        ''' # If no candidates found through LSH, check all texts (fallback)
        if not to_check:
            to_check = set(range(N))
        else:
            # Always add the text itself for checking
            to_check.add(text_index) '''
        
        # Check each candidate for actual similarity
        for candidate_id in to_check:
            if candidate_id != text_index:  # Skip self-comparison
                dist = hamming_distance(sh_main, simhashes[candidate_id])
                if dist <= max_distance:
                    similar_count += 1
        
        print(similar_count)

if __name__ == '__main__':
    main()