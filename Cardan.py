"""
Dawid Madej
----------------------------------------------
Atak na szyfr Kardana metodą wspinaczkową

Atak shotgun hill climbing zaczyna od wielu losowych kluczy i dla każdego z nich próbuje lokalnie poprawiać klucz przez małe mutacje,
wybierając lepsze rozwiązania na podstawie oceny tekstu odszyfrowanego n-gramowym modelem językowym.

Do testów wykorzytsano dwa języki: angielski (26 znaków) oraz kataloński (35 znaków)
----------------------------------------------
Ze względu na dużą liczbę możliwych kluczy przy większych rozmiarach krat, do szyfrowania zastosowano podejście blokowe, co umożliwia
znalezienie poprawnego rozwiązania w rozsądnym czasie przy ataku.

W przypadku użycia do wypełnienia brakujących wartości losowych znaków zamiast pustych pól, skuteczność ataku znacząco spada dla tekstów najkrótszych.
Rozmiar bloku musi zostać zmniejszony do block_n = 7, aby zapewnić możliwość poprawnego odszyfrowania.
"""

import random
import numpy as np

def rotate_coords(n, x, y, times=1):
    for _ in range(times % 4):
        x, y = y, n - 1 - x
    return x, y

def generate_random_key(n):
    center = n // 2
    used = set()
    key_positions = []

    all_positions = [(x, y) for x in range(n) for y in range(n) if (x, y) != (center, center)]
    random.shuffle(all_positions)

    for x, y in all_positions:
        group = sorted(rotate_coords(n, x, y, r) for r in range(4))
        if not any(pos in used for pos in group):
            key_positions.append((x, y))
            used.update(group)
            if len(used) >= n * n - 1:
                break

    return sorted(key_positions)


def encrypt(n, message, key_positions):
    assert len(message) == n * n - 1
    grid = np.full((n, n), '', dtype=str)
    msg_idx = 0

    for rot in range(4):
        for x, y in sorted(rotate_coords(n, *pos, times=rot) for pos in key_positions):
            if (x, y) != (n // 2, n // 2):
                grid[x, y] = message[msg_idx]
                msg_idx += 1

    return ''.join(grid[x, y] for x in range(n) for y in range(n) if (x, y) != (n // 2, n // 2))

def decrypt(n, encrypted_message, key_positions):
    assert len(encrypted_message) == n * n - 1
    grid = np.full((n, n), '', dtype=str)
    idx = 0

    for x in range(n):
        for y in range(n):
            if (x, y) != (n // 2, n // 2):
                grid[x, y] = encrypted_message[idx]
                idx += 1

    decrypted = ''
    for rot in range(4):
        for x, y in sorted(rotate_coords(n, *pos, times=rot) for pos in key_positions):
            if (x, y) != (n // 2, n // 2):
                decrypted += grid[x, y]

    return decrypted

def calculate_min_n(message):
    length = len(message)
    n = 3
    while n * n - 1 < length:
        n += 2
    return n

"""
# Metoda szyfrująca która zamiast losowych znaków dodaje puste pola

def encrypt_message_in_blocks(full_message, key_positions, block_n):
    block_size = block_n * block_n - 1
    padding_len = (block_size - (len(full_message) % block_size)) % block_size

    full_message_padded = full_message + (' ' * padding_len)

    encrypted_blocks = []
    for i in range(0, len(full_message_padded), block_size):
        block = full_message_padded[i:i + block_size]
        encrypted_block = encrypt(block_n, block, key_positions)
        encrypted_blocks.append(encrypted_block)

    return ''.join(encrypted_blocks)
"""

def encrypt_message_in_blocks(full_message, key_positions, block_n = 7, alfabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
    block_size = block_n * block_n - 1

    padding_len = (block_size - (len(full_message) % block_size)) % block_size

    random_padding = ''.join(random.choices(alfabet, k=padding_len))
    full_message_padded = full_message + random_padding

    encrypted_blocks = []
    for i in range(0, len(full_message_padded), block_size):
        block = full_message_padded[i:i + block_size]
        encrypted_block = encrypt(block_n, block, key_positions)
        encrypted_blocks.append(encrypted_block)

    return ''.join(encrypted_blocks)

def decrypt_message_in_blocks(encrypted_full_message, key_positions, block_n = 7):
    block_size = block_n * block_n - 1

    decrypted_blocks = []
    for i in range(0, len(encrypted_full_message), block_size):
        block = encrypted_full_message[i:i + block_size]
        decrypted_block = decrypt(block_n, block, key_positions)
        decrypted_blocks.append(decrypted_block)

    return ''.join(decrypted_blocks).rstrip()
