#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def create_polybius_square(key):
    """
    Create a 6x6 Polybius square for the ADFGVX cipher.
    
    Args:
        key: String with 36 unique characters to fill the grid
        
    Returns:
        A dictionary mapping characters to their coordinates (row, col)
    """
    if len(key) != 36:
        raise ValueError("Key must contain exactly 36 unique characters")
    
    # Check if all characters in the key are unique
    if len(set(key)) != 36:
        raise ValueError("All characters in the key must be unique")
    
    headers = ['A', 'D', 'F', 'G', 'V', 'X']
    square = {}
    
    # Fill the Polybius square
    for i in range(36):
        row = i // 6
        col = i % 6
        char = key[i]
        square[char] = (headers[row], headers[col])
    
    return square

def encrypt(plaintext, polybius_key, transposition_key):
    """
    Encrypt a message using the ADFGVX cipher.
    
    Args:
        plaintext: The message to encrypt
        polybius_key: A string of 36 unique characters for the Polybius square
        transposition_key: The keyword for the transposition step
        
    Returns:
        The encrypted message
    """
    # Normalize input - convert to lowercase and remove spaces
    plaintext = ''.join(c.lower() for c in plaintext if c.isalnum())
    
    # Create the Polybius square
    square = create_polybius_square(polybius_key)
    
    # Substitution step - convert each character to its coordinates
    substituted = []
    for char in plaintext:
        if char in square:
            row, col = square[char]
            substituted.append(row)
            substituted.append(col)
        else:
            # Skip characters not in the Polybius square
            continue
    
    # If no valid characters, return empty string
    if not substituted:
        return ""
    
    # Transposition step
    # 1. Create a matrix with the transposition key as columns
    key_order = sorted(range(len(transposition_key)), key=lambda i: transposition_key[i])
    
    # Calculate number of rows needed
    num_rows = (len(substituted) + len(transposition_key) - 1) // len(transposition_key)
    
    # 2. Fill the matrix column by column
    matrix = [[''] * len(transposition_key) for _ in range(num_rows)]
    
    char_index = 0
    for col in range(len(transposition_key)):
        for row in range(num_rows):
            if char_index < len(substituted):
                matrix[row][col] = substituted[char_index]
                char_index += 1
    
    # 3. Read off the columns according to the key order
    ciphertext = []
    for i in key_order:
        for row in range(num_rows):
            if matrix[row][i]:
                ciphertext.append(matrix[row][i])
    
    return ''.join(ciphertext)

def decrypt(ciphertext, polybius_key, transposition_key):
    """
    Decrypt a message using the ADFGVX cipher.
    
    Args:
        ciphertext: The encrypted message
        polybius_key: A string of 36 unique characters for the Polybius square
        transposition_key: The keyword for the transposition step
        
    Returns:
        The decrypted message
    """
    # Check if ciphertext contains only valid ADFGVX characters
    valid_chars = set('ADFGVX')
    if not all(c in valid_chars for c in ciphertext):
        raise ValueError("Ciphertext contains invalid characters. Only A, D, F, G, V, X are allowed.")
    
    # If ciphertext length is odd, it's invalid
    if len(ciphertext) % 2 != 0:
        raise ValueError("Invalid ciphertext length. ADFGVX ciphertext must have even length.")
    
    # Create the Polybius square
    square = create_polybius_square(polybius_key)
    
    # Reverse the square for decryption (coordinates to character)
    reverse_square = {(row, col): char for char, (row, col) in square.items()}
    
    # Calculate dimensions for the transposition matrix
    key_length = len(transposition_key)
    full_columns = len(ciphertext) % key_length
    if full_columns == 0:
        full_columns = key_length
    
    num_rows = len(ciphertext) // key_length
    if full_columns < key_length:
        num_rows += 1
    
    # Get the order of columns based on the transposition key
    key_order = sorted(range(len(transposition_key)), key=lambda i: transposition_key[i])
    sorted_indices = [0] * len(transposition_key)
    for i, pos in enumerate(key_order):
        sorted_indices[pos] = i
    
    # Calculate column lengths
    col_lengths = [num_rows if i < full_columns else num_rows - 1 for i in range(key_length)]
    
    # Reverse the transposition
    matrix = [[''] * key_length for _ in range(num_rows)]
    char_index = 0
    
    # Fill columns according to the key order
    for i in range(key_length):
        col = sorted_indices[i]
        for row in range(col_lengths[col]):
            if char_index < len(ciphertext):
                matrix[row][col] = ciphertext[char_index]
                char_index += 1
    
    # Read the matrix row by row
    transposed = []
    for row in range(num_rows):
        for col in range(key_length):
            if matrix[row][col]:
                transposed.append(matrix[row][col])
    
    # Reverse the substitution
    plaintext = []
    for i in range(0, len(transposed), 2):
        if i + 1 < len(transposed):
            row, col = transposed[i], transposed[i+1]
            if (row, col) in reverse_square:
                plaintext.append(reverse_square[(row, col)])
    
    return ''.join(plaintext)

def generate_default_polybius_key():
    """
    Generate a default key for the Polybius square containing alphanumeric characters.
    
    Returns:
        A string with 36 unique characters (alphabets and digits)
    """
    # Use alphabets (a-z) and digits (0-9) to create a 36-character key
    import string
    return string.ascii_lowercase + string.digits[:10]

