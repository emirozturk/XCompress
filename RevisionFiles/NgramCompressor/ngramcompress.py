import os
import heapq
import argparse
from collections import Counter


class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
    
    def __lt__(self, other):
        return self.freq < other.freq


def build_huffman_tree(freqs):
    priority_queue = [Node(char, freq) for char, freq in freqs.items()]
    heapq.heapify(priority_queue)
    
    while len(priority_queue) > 1:
        left = heapq.heappop(priority_queue)
        right = heapq.heappop(priority_queue)
        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(priority_queue, merged)
    
    root = priority_queue[0]
    huffman_codes = {}
    
    def generate_codes(node, code=""):
        if node is not None:
            if node.char is not None:
                huffman_codes[node.char] = code
            generate_codes(node.left, code + "0")
            generate_codes(node.right, code + "1")
    
    generate_codes(root)
    return root, huffman_codes


def serialize_tree(node):
    if node is None:
        return '0'
    if node.char is not None:
        ngram_len = len(node.char)
        return '1' + chr(ngram_len) + node.char.decode('latin1')
    return '0' + serialize_tree(node.left) + serialize_tree(node.right)


def deserialize_tree(data):
    def _deserialize(index):
        if data[index] == '0':
            left_node, next_index = _deserialize(index + 1)
            right_node, next_index = _deserialize(next_index)
            node = Node(None, 0)
            node.left = left_node
            node.right = right_node
            return node, next_index
        else:
            ngram_len = ord(data[index + 1])
            ngram = data[index + 2:index + 2 + ngram_len].encode('latin1')
            return Node(ngram, 0), index + 2 + ngram_len
    root, _ = _deserialize(0)
    return root


def encode_data(data, codes, n):
    encoded = []
    i = 0
    while i < len(data) - n + 1:
        ngram = data[i:i+n]
        encoded.append(codes[ngram])
        i += n
    return ''.join(encoded)


def decode_data(encoded_data, codes):
    reverse_codes = {v: k for k, v in codes.items()}
    decoded_data = bytearray()
    code = ""
    
    for bit in encoded_data:
        code += bit
        if code in reverse_codes:
            decoded_data.extend(reverse_codes[code])
            code = ""
    
    return bytes(decoded_data)


def pad_data(data, n):
    padding_length = (n - len(data) % n) % n
    return data + b'\x00' * padding_length


def process_files(input_file, output_file, n, mode):
    file_path = input_file
    with open(file_path, 'rb') as f:
        data = f.read()

    data = pad_data(data, n)

    if mode == 'compress':
        ngrams = Counter(data[i:i+n] for i in range(len(data) - n + 1))
        
        root, huffman_codes = build_huffman_tree(ngrams)
        
        serialized_tree = serialize_tree(root)
        serialized_tree_bytes = serialized_tree.encode('latin1')
        tree_size = len(serialized_tree_bytes)
        
        encoded_data = encode_data(data, huffman_codes, n)
        
        # Pad encoded_data to be a multiple of 8 bits
        padding_length = (8 - len(encoded_data) % 8) % 8
        encoded_data += '0' * padding_length
        
        # Convert encoded_data to bytes
        byte_array = bytearray()
        for i in range(0, len(encoded_data), 8):
            byte = encoded_data[i:i+8]
            byte_array.append(int(byte, 2))

        with open(output_file, 'wb') as out_file:
            out_file.write(tree_size.to_bytes(4, byteorder='big'))
            out_file.write(serialized_tree_bytes)
            out_file.write(padding_length.to_bytes(1, byteorder='big'))
            out_file.write(byte_array)

    elif mode == 'decompress':
        with open(input_file, 'rb') as in_file:
            tree_size = int.from_bytes(in_file.read(4), byteorder='big')
            serialized_tree_bytes = in_file.read(tree_size)
            serialized_tree = serialized_tree_bytes.decode('latin1')
            padding_length = int.from_bytes(in_file.read(1), byteorder='big')
            encoded_bytes = in_file.read()
        
        encoded_data = ''.join(f'{byte:08b}' for byte in encoded_bytes)
        encoded_data = encoded_data[:-padding_length]  # Remove padding

        root = deserialize_tree(serialized_tree)
        
        huffman_codes = {}
        def generate_codes(node, code=""):
            if node is not None:
                if node.char is not None:
                    huffman_codes[node.char] = code
                generate_codes(node.left, code + "0")
                generate_codes(node.right, code + "1")
        generate_codes(root)
        
        decoded_data = decode_data(encoded_data, huffman_codes)
        
        with open(output_file, 'wb') as out_file:
            out_file.write(decoded_data)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Compress or decompress files using n-grams.')
    parser.add_argument('filename', help='The input file to be processed')
    parser.add_argument('-n', type=int, default=4, help='The value of n for n-grams')
    parser.add_argument('outputfilename', nargs='?', help='The output file name (optional)')
    parser.add_argument('-c', '--compress', action='store_true', help='Compress the file')
    parser.add_argument('-d', '--decompress', action='store_true', help='Decompress the file')

    args = parser.parse_args()

    if args.compress:
        mode = 'compress'
        if not args.outputfilename:
            output_file = args.filename + '.ngram'
        else:
            output_file = args.outputfilename
    elif args.decompress:
        mode = 'decompress'
        if not args.outputfilename:
            output_file = args.filename.replace(".ngram", ".o")
        else:
            output_file = args.outputfilename
    else:
        raise ValueError("You must specify either --compress or --decompress.")

    process_files(args.filename, output_file, args.n, mode)