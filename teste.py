from models.trie import Trie
from models.radix import RadixTree

list_trie = Trie()
list_radix = RadixTree()

# with open('data/verbos', 'r') as file:
#     words_list = file.read().split('\n')

# for word in words_list:
#     list_trie.insert(word)
    # list_radix.insert(word)

# print(list_trie.count_nodes())
# print(list_radix.count_nodes())

print(list_trie.insert("teste"))
print(list_trie.insert("teste"))
print(list_trie.insert("testou"))

# print(list_trie.search("teste"))
# print(list_trie.matches("teste"))
print(list_trie.generate_tree())
print(list_trie.remove("teste"))
# print(list_trie.remove("teste"))

# print(list_trie.search("teste"))
# print(list_trie.matches("teste"))

print(list_trie.generate_tree())