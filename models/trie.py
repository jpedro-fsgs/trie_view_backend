
class TrieNode:
    def __init__(self):
        self.children = {}
        self.word = None


class Trie:
    def __init__(self):
        self.root = TrieNode()
        self.tree_view = self.generate_tree()

    def clear(self):
        self.root = TrieNode()
        self.tree_view = self.generate_tree()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]

        if node.word == word:
            return False
        node.word = word

        self.tree_view = self.generate_tree()
        return True

    def remove(self, word):
        stack = []
        node = self.root
        
        for char in word:
            if char not in node.children:
                return False
            stack.append((char, node))
            node = node.children[char]

        if node.word != word:
            return False
        
        node.word = None

        while stack:
            char, parent = stack.pop()
            child = parent.children[char]

            if child.word is not None or child.children:
                break

            del parent.children[char]

        self.tree_view = self.generate_tree()
        return True

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.word == word

    def matches(self, word, limit=50):
        node = self.root
        matches_list = []

        for char in word:
            if char not in node.children:
                return matches_list
            node = node.children[char]
        
        stack = [node]

        while stack:
            if len(matches_list) > limit:
                return matches_list

            current_node = stack.pop()
            if current_node.word:
                matches_list.append(current_node.word)
            stack.extend(current_node.children.values())

        return matches_list
    
    def count_nodes(self):
        count = 0
        stack = [self.root]

        while stack:
            current = stack.pop()
            stack.extend(current.children.values())
            count += 1

        return count


    def generate_tree(self):

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
    
    def get_tree(self):
        return self.tree_view