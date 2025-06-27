import concurrent.futures
import random
import time
from ngram import Ngram_score
from Cardan import (
    generate_random_key,
    rotate_coords,
    calculate_min_n,
    encrypt_message_in_blocks,
    decrypt_message_in_blocks
)

NGRAM_SCORER = Ngram_score('english_bigrams/my_english_bigrams.csv', sep=' ')
# NGRAM_SCORER = Ngram_score('catalan_bigrams/my_catalan_bigrams.csv')

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

    available_positions = [
        (x, y) for x in range(n) for y in range(n)
        if (x, y) != (center, center)
    ]
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

def shotgun_hill_climbing_run(encrypted, ngram_model, n, timelimit=10, wait_to_progress=0.2, simulation_id=0):
    best_key = generate_random_key(n)
    best_decryption = decrypt_message_in_blocks(encrypted, best_key, n)
    best_score = ngram_model.score(best_decryption)

    t0 = time.time()

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

                if new_score > best_score:
                    best_key = new_key
                    best_score = new_score
                    best_decryption = new_decryption

    return {
        "id": simulation_id,
        "score": best_score,
        "key": best_key,
        "decryption": best_decryption[:200]
    }

def normalize_text(file, alfabet):
    with open(file, 'r', encoding='utf-8') as f:
        text = f.read()
    text = text.upper()
    normalized_text = ''.join([char for char in text if char in alfabet])
    return normalized_text

def run_parallel_simulations(path_to_file, num_simulations=40, block_n=9):
    alfabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    # alfabet = 'AÀBCÇDEÈÉFGHIÍÏJKLMNOÒÓPQRSTUÚÜVWXYZ'

    message = normalize_text(path_to_file, alfabet)
    print("Normalized message length:", len(message))

    n = calculate_min_n(message)
    true_key = generate_random_key(block_n)
    encrypted_message = encrypt_message_in_blocks(message, n, true_key, block_n)

    print("Starting simulations...\n")

    results = []
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [
            executor.submit(
                shotgun_hill_climbing_run,
                encrypted_message,
                NGRAM_SCORER,
                block_n,
                20,
                0.2,
                i
            )
            for i in range(num_simulations)
        ]

        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            print(f"\n--- Symulacja #{result['id']} ---")
            print(f"Score: {result['score']:.4f}")
            print(f"Key: {result['key']}")
            print(f"Decryption snippet: {result['decryption']}")
            results.append(result)

    return results

if __name__ == "__main__":
    run_parallel_simulations('english_bigrams/test/test600.txt', num_simulations=40, block_n=9)
