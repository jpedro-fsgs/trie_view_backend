class TrieNode:
    def __init__(self):
        self.children = {}
        self.word = None


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.word = word

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.word
    
    def matches(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return []
            node = node.children[char]

        def get_matches(node):
            result = [child_node.word for child_node in node.children.values() if child_node.word]
            for child_node in node.children.values():
                result += get_matches(child_node)
            return result

        return get_matches(node)

        



    # def get_tree(self):
    #     def build_tree(node):
    #         tree = {"name": "Root", "children": []}
    #         for char, child_node in node.children.items():
    #             subtree = {
    #                 "name": char,
    #                 "is_end_of_word": node.is_end_of_word,
    #                 "children": build_tree(child_node)["children"],
    #             }
    #             tree["children"].append(subtree)
    #         return tree

    #     return build_tree(self.root)


# Exemplo de uso:
trie = Trie()
trie.insert("chat")
trie.insert("chatbot")
trie.insert("chatt")
trie.insert("rato")
trie.insert("coelho")
trie.insert("coe")

print(trie.search("rato"))
print(trie.search("coelho"))
print(trie.search("coe"))
print(trie.search("r"))
print(trie.search("ra"))

print(trie.matches("co"))

# import json

# tree_json = json.dumps(trie.get_tree(), indent=2)
# print(tree_json)
