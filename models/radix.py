class RadixTreeNode:
    def __init__(self, key=""):
        self.key = key
        self.children = {}
        self.word = None


class RadixTree:
    def __init__(self):
        self.root = RadixTreeNode()
        self.block_insertion = False
        self.tree_view = self.generate_tree()

    def clear(self):
        self.root = RadixTreeNode()
        self.tree_view = self.generate_tree()

    @staticmethod
    def _common_prefix(str1, str2):
        min_length = min(len(str1), len(str2))
        for i in range(min_length):
            if str1[i] != str2[i]:
                return str1[:i]
        return str1[:min_length]

    def insert(self, word):
        node = self.root
        index = 0

        while index < len(word):
            found_prefix = False

            # Iteramos sobre uma cópia dos itens para permitir modificações no dicionário
            for edge, child in list(node.children.items()):
                common_prefix = self._common_prefix(word[index:], edge)

                if common_prefix:
                    found_prefix = True

                    if common_prefix == edge:
                        # Se o prefixo comum coincide com toda a aresta, seguimos para o nó filho
                        node = child
                        index += len(common_prefix)
                        break
                    else:
                        # Caso haja apenas correspondência parcial, é necessário dividir o nó existente.
                        remaining_edge = edge[len(common_prefix):]
                        remaining_word = word[index + len(common_prefix):]

                        # Cria um novo nó para a parte restante da aresta existente
                        new_child = RadixTreeNode(remaining_edge)
                        new_child.children = child.children
                        new_child.word = child.word

                        # Atualiza o nó filho para representar o prefixo comum
                        child.key = common_prefix
                        child.children = {remaining_edge: new_child}
                        child.word = None

                        # Atualiza o dicionário do nó pai:
                        # Remove a chave antiga e insere a nova chave (prefixo comum)
                        node.children.pop(edge)
                        node.children[common_prefix] = child

                        # Se ainda houver parte da palavra a inserir, adicionamos um novo nó
                        if remaining_word:
                            child.children[remaining_word] = RadixTreeNode(remaining_word)
                            child.children[remaining_word].word = word
                        else:
                            # Caso contrário, marcamos o nó atual como final da palavra
                            child.word = word

                        self.tree_view = self.generate_tree()
                        return True

            # Se não foi encontrado nenhum prefixo comum, adicionamos um novo nó
            if not found_prefix:
                remaining_word = word[index:]
                node.children[remaining_word] = RadixTreeNode(remaining_word)
                node.children[remaining_word].word = word
                self.tree_view = self.generate_tree()
                return True

        # Se chegamos ao final da palavra, verificamos se ela já está presente
        if node.word == word:
            return False  # Palavra já existe

        node.word = word
        self.tree_view = self.generate_tree()
        return True


    def remove(self, word):
        """
        Remove a palavra 'word' da árvore, se ela existir.
        Percorre a árvore consumindo partes da palavra de acordo com as chaves dos nós.
        """
        node = self.root
        stack = []  # Armazena os pares (nó pai, aresta utilizada, nó filho) para retroceder
        remaining = word

        # Percorre a árvore comparando partes da palavra com as chaves dos nós
        while remaining:
            found = False
            for edge, child in node.children.items():
                if remaining.startswith(edge):
                    stack.append((node, edge, child))
                    node = child
                    remaining = remaining[len(edge):]
                    found = True
                    break
            if not found:
                return False  # Palavra não encontrada
        
        # Se a palavra não está marcada no nó final, ela não foi inserida exatamente
        if node.word != word:
            return False

        # Desmarca a palavra no nó final
        node.word = None

        # Remove nós desnecessários (folhas sem palavra armazenada e sem filhos)
        while stack:
            parent, edge, child = stack.pop()
            if child.word is None and not child.children:
                del parent.children[edge]
            else:
                break

        self.tree_view = self.generate_tree()
        return True


    def search(self, word):
        """
        Busca a palavra 'word' na árvore.
        Retorna True se a palavra estiver presente (exata) ou False caso contrário.
        """
        node = self.root
        remaining = word

        # Percorre a árvore consumindo partes da palavra conforme as chaves dos nós
        while remaining:
            found = False
            for edge, child in node.children.items():
                if remaining.startswith(edge):
                    remaining = remaining[len(edge):]
                    node = child
                    found = True
                    break
            if not found:
                return False  # Caminho para a palavra não foi encontrado

        # Verifica se o nó final marca o término da palavra buscada
        return node.word == word


    def matches(self, prefix, limit=50):
        """
        Retorna uma lista (com até 50 itens) de palavras armazenadas na árvore 
        que começam com o prefixo fornecido.
        Primeiro, localiza o nó correspondente ao prefixo e, em seguida, percorre a subárvore.
        """
        node = self.root
        remaining = prefix

        # Localiza o nó que corresponde ao prefixo (podendo estar no meio de uma aresta)
        while remaining:
            found = False
            for edge, child in node.children.items():
                if remaining.startswith(edge):
                    remaining = remaining[len(edge):]
                    node = child
                    found = True
                    break
                elif edge.startswith(remaining):
                    # O prefixo está no meio da aresta; podemos considerar esse filho como ponto de partida
                    node = child
                    remaining = ""
                    found = True
                    break
            if not found:
                return []  # Prefixo não encontrado

        # A partir do nó correspondente, faz uma busca em largura (BFS) para coletar as palavras
        matches_list = []
        queue = [node]
        while queue and len(matches_list) < limit:
            current = queue.pop(0)
            if current.word is not None:
                matches_list.append(current.word)
            queue.extend(current.children.values())

        return matches_list
    
    def count_nodes(self):
        count = 0
        queue = [self.root]

        while queue:
            current = queue.pop()
            queue.extend(current.children.values())
            count += 1

        return count

    def generate_tree(self):

        def build_tree(node):
            return sorted([
                {
                    "name": key,
                    "children": build_tree(child_node),
                    **({"attributes": {"word": child_node.word}} if child_node.word else {})
                }
                for key, child_node in node.children.items()
            ], key=lambda n: n["name"])

        return {"name": "Root", "children": build_tree(self.root)}

    def get_tree(self):
        return self.tree_view