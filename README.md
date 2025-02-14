# Trie View Backend

This is the backend for the Trie View application, built with FastAPI. It provides endpoints to interact with a trie data structure, including inserting words, matching prefixes, and generating a tree representation.

## Endpoints

### GET /match/{word}

Returns a list of words that match the given prefix.

- **Parameters**: 
  - `word` (string): The prefix to match.
- **Response**:
  - `length` (integer): The number of matching words.
  - `results` (list of strings): The matching words.

### POST /insert/{word}

Inserts a word into the public trie. If the word matches the clear password, it clears the trie.

- **Parameters**: 
  - `word` (string): The word to insert or the clear password.
- **Response**: None

### GET /tree

Generates a tree representation of the public trie.

- **Response**:
  - A JSON object representing the trie structure.


## Data

The initial list of words is loaded from the `data/palavras` file.
