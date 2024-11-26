# import heapq
# from collections import defaultdict

# class Node:
#     def __init__(self, frequency, symbol=None, left=None, right=None):
#         self.frequency = frequency
#         self.symbol = symbol
#         self.left = left
#         self.right = right
    
#     def __lt__(self, other):
#         # Compare based on frequency first, then lexicographically
#         if self.frequency == other.frequency:
#             return self.symbol < other.symbol
#         return self.frequency < other.frequency

# def Huffman(s):
#     # Step 1: Count frequency of each character
#     frequency = defaultdict(int)
#     for char in s:
#         frequency[char] += 1
#     print(frequency)
#     # Step 2: Create priority queue
#     heap = [Node(freq, sym) for sym, freq in frequency.items()]
#     heapq.heapify(heap)
    
#     # Step 3: Build Huffman Tree
#     while len(heap) > 1:
#         x = heapq.heappop(heap)
#         y = heapq.heappop(heap)
        
#         # Create a new parent node
#         new_node = Node(x.frequency + y.frequency, x.symbol + y.symbol, x, y)
#         heapq.heappush(heap, new_node)
    
#     # The root of the Huffman Tree
#     root = heap[0]
    
#     # Step 4: Generate codes by traversing the tree
#     def generate_codes(node, current_code, codes):
#         if node is None:
#             return
        
#         # If it's a leaf node, assign the code
#         if node.left is None and node.right is None:
#             codes[node.symbol] = current_code
#             return
        
#         generate_codes(node.left, current_code + "0", codes)
#         generate_codes(node.right, current_code + "1", codes)
    
#     codes = {}
#     generate_codes(root, "", codes) 
#     return codes

# # Example usage
# s = "aaaaaaaabcdeffedcccccccccccba"
# huffman_codes = Huffman(s)
# print(huffman_codes)
from werkzeug.security import generate_password_hash
print(generate_password_hash("ankit"))
from datetime import datetime
print(datetime.now())
