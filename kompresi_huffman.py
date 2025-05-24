import heapq
import pickle
from collections import Counter

class HuffmanNode:
    def __init__(self, byte=None, freq=0):
        self.byte = byte
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_tree(data):
    frequency = Counter(data)
    heap = [HuffmanNode(byte, freq) for byte, freq in frequency.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(freq=left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)

    return heap[0]

def generate_codes(node, prefix="", codebook={}):
    if node:
        if node.byte is not None:
            codebook[node.byte] = prefix
        generate_codes(node.left, prefix + "0", codebook)
        generate_codes(node.right, prefix + "1", codebook)
    return codebook

def pad_bits(bitstring):
    extra = 8 - len(bitstring) % 8
    padded_info = f'{extra:08b}'
    return padded_info + bitstring + '0' * extra

def unpad_bits(padded):
    extra = int(padded[:8], 2)
    return padded[8:-extra] if extra > 0 else padded[8:]

def encode_png_file(input_file, output_file):
    with open(input_file, 'rb') as f:
        data = f.read()

    tree = build_tree(data)
    codes = generate_codes(tree)
    bitstring = ''.join(codes[b] for b in data)
    padded_bits = pad_bits(bitstring)

    compressed = bytearray()
    for i in range(0, len(padded_bits), 8):
        compressed.append(int(padded_bits[i:i+8], 2))

    with open(output_file, 'wb') as f:
        pickle.dump((tree, compressed), f)

    print(f"PNG '{input_file}' berhasil dikompresi menjadi '{output_file}'.")

def decode_png_file(input_file, output_file):
    with open(input_file, 'rb') as f:
        tree, compressed = pickle.load(f)

    bits = ''.join(f'{byte:08b}' for byte in compressed)
    bitstream = unpad_bits(bits)

    current = tree
    decoded_bytes = bytearray()

    for bit in bitstream:
        current = current.left if bit == '0' else current.right
        if current.byte is not None:
            decoded_bytes.append(current.byte)
            current = tree

    with open(output_file, 'wb') as f:
        f.write(decoded_bytes)

    print(f"File '{input_file}' berhasil didekompresi menjadi '{output_file}'.")

# Penggunaan
if __name__ == '__main__':
    # Ganti dengan nama file PNG
    encode_png_file("sample/sample10.png", "sample/sample10_png.huff")
    decode_png_file("sample/sample10_png.huff", "compressed/sample10_compressed.png")
