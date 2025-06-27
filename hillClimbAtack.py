from ngram import Ngram_score
import time
import random

from Cardan import (
    generate_random_key,
    rotate_coords,
    calculate_min_n,
    encrypt_message_in_blocks,
    decrypt_message_in_blocks
)

NGRAM_SCORER = Ngram_score('english_bigrams/my_english_bigrams.csv')
alfabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# NGRAM_SCORER = Ngram_score('catalan_bigrams/my_catalan_bigrams.csv')
# alfabet = 'AÀBCÇDEÈÉFGHIÍÏJKLMNOÒÓPQRSTUÚÜVWXYZ'


def mutate_key(n, key):
    new_key = key.copy()
    used = set()
    center = n // 2

    for x, y in new_key:
        for r in range(4):
            used.add(rotate_coords(n, x, y, r))

    idx_to_replace = random.randint(0, len(new_key) - 1)
    old_pos = new_key[idx_to_replace]

    for r in range(4):
        used.discard(rotate_coords(n, *old_pos, r))

    available_positions = []
    for x in range(n):
        for y in range(n):
            if (x, y) != (center, center):
                available_positions.append((x, y))

    random.shuffle(available_positions)

    for candidate in available_positions:
        if candidate == old_pos:
            continue

        group = [rotate_coords(n, *candidate, r) for r in range(4)]
        if not any(p in used for p in group):
            new_key[idx_to_replace] = candidate
            break
    else:
        new_key[idx_to_replace] = old_pos

    return sorted(new_key)

def shotgun_hill_climbing(encrypted, ngram_model, n, timelimit=10, wait_to_progress=0.2):
    best_key = generate_random_key(n)
    best_decryption = decrypt_message_in_blocks(encrypted, best_key, n)
    best_score = ngram_model.score(best_decryption)

    t0 = time.time()
    start_time = time.time()

    print(f"Początkowy klucz: {best_key}")
    print(f"Początkowy dekrypt: {best_decryption}...\n")

    while time.time() - t0 < timelimit:
        current_key = generate_random_key(n)
        current_decryption = decrypt_message_in_blocks(encrypted, current_key, n)
        current_score = ngram_model.score(current_decryption)

        time_progress = time.time()

        while time.time() - time_progress < wait_to_progress:
            new_key = mutate_key(n, current_key)
            new_decryption = decrypt_message_in_blocks(encrypted, new_key, n)
            new_score = ngram_model.score(new_decryption)

            if new_score > current_score:
                current_key = new_key
                current_score = new_score
                current_decryption = new_decryption
                time_progress = time.time()

                print(f"Lepszy lokalny wynik! Aktualny score: {current_score:.4f} oraz tekst: {current_decryption[:80]}... Best wynik: {best_score} oraz tekst: {best_decryption[:80]}")

                if new_score > best_score:
                    best_key = new_key
                    best_score = new_score
                    best_decryption = new_decryption

    print(f"Najlepszy wynik końcowy: {best_score:.4f}")
    print(f"Klucz: {best_key}")
    print(f"Dekrypt: {best_decryption}\n")

    elapsed = time.time() - start_time
    minutes = int(elapsed // 60)
    seconds = elapsed % 60
    print(f"Czas: {minutes}m {seconds:.2f}s...\n")

    return best_decryption

def normalize_text(file, alfabet):
    with open(file, 'r', encoding='utf-8') as f:
        text = f.read()
    text = text.upper()
    normalized_text = ''.join([char for char in text if char in alfabet])
    return normalized_text

message = normalize_text('english_bigrams/test/test1000.txt', alfabet)
# message = normalize_text('catalan_bigrams/test/test1000.txt', alfabet)

n = calculate_min_n(message)
block_n = 7

true_key = generate_random_key(block_n)
encrypted_message = encrypt_message_in_blocks(message, n, true_key, block_n)

best_decryption = shotgun_hill_climbing(encrypted_message, NGRAM_SCORER, block_n)
print('Is the same = ', message[:60] == best_decryption[:60])

"""
Testy były robione dla tekstów koło 600, 1000 i 1600 znaków. 
Dla każdego wartość ustawiona została na timelimit = 20 oraz wait_to_progress = 0.2.
Każdy rodzaj był przetestowany 40 razy.

---------------------------------------------------------
Angielski:

block_n = 9 / 7:
600 znaków - 52.5% / 100% rozwiązywalności
1000 znaków - 72.5% / 97.5% rozwiązywalności
1600 znaków - 50% /  98% rozwiązywalności
---------------------------------------------------------
Kataloński:

block_n = 9 / 7:
600 znaków - 60% / 100% rozwiązywalności
1000 znaków - 70% / 97.5% rozwiązywalności
1600 znaków - 25% /  97.5% rozwiązywalności
---------------------------------------------------------
Dla block_n = 9 istnieje szansa na to, że atak znajdzie odpowiedni klucz, jednak dla block_n = 7 robi to z wiele większą szansą na powodzenie.
"""