class TrieNode:
    def __init__(self):
        self.children = {}
        self.word = None


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def clear(self):
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

        matches_list = []
        queue = []
        queue.append(node)

        while queue:
            if len(matches_list) > 50:
                return matches_list

            current_node = queue.pop()
            if current_node.word:
                matches_list.append(current_node.word)
            queue.extend(current_node.children.values())

        return matches_list

    def get_tree(self):

        def build_tree(node):
            return [
                {
                    "name": char,
                    "children": build_tree(child_node),
                    **({"attributes": {"word": child_node.word}} if child_node.word else {})
                }
                for char, child_node in node.children.items()
            ]

        return {"name": "Root", "children": build_tree(self.root)}
