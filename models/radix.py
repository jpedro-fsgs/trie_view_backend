class RadixTreeNode:
    def __init__(self, key=""):
        self.key = key
        self.children = {}
        self.word = None


class RadixTree:
    def __init__(self):
        self.root = RadixTreeNode()

    def clear(self):
        self.root = RadixTreeNode()

    

    def insert(self, word):
        def _common_prefix(str1, str2):
            min_length = min(len(str1), len(str2))
            for i in range(min_length):
                if str1[i] != str2[i]:
                    return str1[:i]
                
            return str1[:min_length]

        node = self.root
        index = 0
        while index < len(word):
            for key, child in node.children.items():
                common_prefix = self._common_prefix(word[index:], key)

                if common_prefix:
                    if common_prefix == key:
                        # Segue para o próximo nó se o prefixo corresponde exatamente à chave do nó
                        node = child
                        index += len(common_prefix)
                        break
                    else:
                        # Divide o nó existente
                        remaining_key = key[len(common_prefix):]
                        new_child = RadixTreeNode(remaining_key)
                        new_child.children = child.children
                        new_child.word = child.word

                        child.key = common_prefix
                        child.children = {remaining_key: new_child}
                        child.word = None  # O prefixo agora não é mais uma palavra completa

                        # Continua a inserção para a parte restante da palavra
                        node = child
                        index += len(common_prefix)
                        break
            else:
                # Nenhum prefixo comum encontrado, adicionamos um novo nó
                node.children[word[index:]] = RadixTreeNode(word[index:])
                node.children[word[index:]].word = word
                return True

        if node.word == word:
            return False  # Palavra já existe
        node.word = word
        return True



    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.word

    def matches(self, word):
        node = self.root

                

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
    
    def count_nodes(self):
        count = 0
        queue = [self.root]

        while queue:
            current = queue.pop()
            queue.extend(current.children.values())
            count += 1

        return count

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
