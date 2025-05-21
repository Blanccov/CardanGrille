import random
import time

from ngram import Ngram


# Funkcja do obrotu współrzędnych
def rotate_coords(n, x, y, times=1):
    for _ in range(times % 4):
        x, y = y, n - 1 - x
    return x, y

# Funkcja do generowania losowego klucza
def generate_random_grill_key(n):
    center = n // 2
    used = set()
    key_positions = []

    # Lista wszystkich możliwych pozycji na kluczu (poza środkiem)
    all_positions = [(x, y) for x in range(n) for y in range(n) if (x != center or y != center)]

    # Losowanie pozycji
    random.shuffle(all_positions)

    for x, y in all_positions:
        group = set(rotate_coords(n, x, y, r) for r in range(4))
        if not group & used:
            key_positions.append((x, y))
            used |= group
        if len(used) >= n * n - 1:
            break

    # Posortowanie pozycji bez użycia lambda
    key_positions.sort()

    return key_positions

# Funkcja do wyświetlania gridu
def print_grid(grid):
    for row in grid:
        print(' '.join(cell if cell else '.' for cell in row))
    print()

# Funkcja do rysowania klucza na gridzie
def print_key_grid(n, key_positions, rot=0):
    center = n // 2
    grid = [['.' for _ in range(n)] for _ in range(n)]
    for x, y in key_positions:
        rx, ry = rotate_coords(n, x, y, rot)
        grid[rx][ry] = '•'
    grid[center][center] = 'X'  # środek
    print("📍 Klucz jako kratka:")
    print_grid(grid)

# Funkcja do szyfrowania
def encrypt_with_grill_verbose(n, message, key_positions):
    assert len(message) == n * n - 1, "Wiadomość musi mieć dokładnie n² - 1 znaków"
    grid = [['' for _ in range(n)] for _ in range(n)]
    msg_idx = 0

    print("🔐 Proces szyfrowania:")

    # Tworzenie szyfrogramu przez rotacje
    for rot in range(4):
        print(f"🌀 Rotacja {rot * 90}°:")
        # Rotujemy współrzędne klucza
        rotated_key_positions = [rotate_coords(n, x, y, rot) for x, y in key_positions]
        rotated_key_positions.sort()

        print_key_grid(n, key_positions, rot)  # Wizualizacja klucza

        for i, (x, y) in enumerate(rotated_key_positions):
            if (x, y) == (n // 2, n // 2):
                continue  # Ignorujemy środek
            grid[x][y] = message[msg_idx]
            print(f"  Wpisuję '{message[msg_idx]}' → pole ({x},{y})")
            msg_idx += 1
        print_grid(grid)

    # Odczytanie zaszyfrowanej wiadomości: odczytujemy z siatki
    encrypted_message_str = ''.join(grid[x][y] for x in range(n) for y in range(n) if (x, y) != (n // 2, n // 2))
    return encrypted_message_str

# Funkcja do deszyfrowania
def decrypt_with_grill_verbose(n, encrypted_message, key_positions):
    assert len(encrypted_message) == n * n - 1, "Zaszyfrowana wiadomość musi mieć dokładnie n² - 1 znaków"

    # Tworzymy grid z załadowanymi literami z wiadomości
    grid = [['' for _ in range(n)] for _ in range(n)]
    decrypt_grid = [['' for _ in range(n)] for _ in range(n)]
    msg_idx = 0

    # Ładujemy wiadomość do grida (pomijając środek)
    for x in range(n):
        for y in range(n):
            if (x, y) != (n // 2, n // 2):
                grid[x][y] = encrypted_message[msg_idx]
                decrypt_grid[x][y] = encrypted_message[msg_idx]
                msg_idx += 1

    # print("🔓 Proces deszyfrowania:")

    decrypted_message = ""

    # Odczytujemy litery z grida na podstawie rotacji klucza
    for rot in range(4):
        # print(f"🌀 Rotacja {rot * 90}°:")

        # Rotujemy współrzędne klucza
        rotated_key_positions = [rotate_coords(n, x, y, rot) for x, y in key_positions]
        rotated_key_positions.sort()

        # Wizualizacja grida i klucza
        # print_key_grid(n, key_positions, rot)  # Wizualizacja klucza
        # print_grid(decrypt_grid)  # Można pokazać grid po wszystkich rotacjach

        # Odczytujemy wiadomość, korzystając z otworów w kluczu
        for x, y in rotated_key_positions:
            if (x, y) == (n // 2, n // 2):
                continue  # Ignorujemy środek
            decrypted_message += grid[x][y]
            decrypt_grid[x][y] = '.'
            # print(f"  Odczytuję '{grid[x][y]}' → pole ({x},{y})")

    return decrypted_message

# Funkcja do dostosowania długości wiadomości
def adjust_message_length(n, message):
    required_length = n * n - 1
    if len(message) < required_length:
        # Jeśli wiadomość jest za krótka, uzupełnij ją spacjami
        message = message.ljust(required_length)
    elif len(message) > required_length:
        # Jeśli wiadomość jest za długa, przytnij ją
        message = message[:required_length]
    return message

# 🔧 Parametry
n = 15  # Można ustawić na dowolną liczbę nieparzystą
message = "ENGLISHTEXTSFORBEGINNERSTOPRACTICEREADINGANDCOMPREHENSIONONLINEANDFORFREEPRACTICINGYOURCOMPREHENSIONOFWRITTENENGLISHWILLBOTHIMPROVEYOURVOCABULARYANDUNDERSTANDINGOFGRAMMARANDWORDORDERTHETEXTSBELOWAREDESIGNEDTOHELPYOUDEVELOPWHILEGIVINGYOUANINSTANTEVALUATIONOFYOURPROGRESS"  # Można podać dowolną wiadomość

# Dostosowanie długości wiadomości
message = adjust_message_length(n, message)

# 🔑 Generowanie losowego klucza
key = generate_random_grill_key(n)
print("🗝️  Losowy klucz (otwory):")
for x, y in key:
    print(f"  ({x},{y})")
print()

# 🔐 Szyfrowanie z wypisywaniem kroków
encrypted_message = encrypt_with_grill_verbose(n, message, key)
print(f"🔒 Zaszyfrowana wiadomość: {encrypted_message}")

# Przykład deszyfrowania
decrypted_message = decrypt_with_grill_verbose(n, encrypted_message, key)
print(f"🔑 Odszyfrowana wiadomość: {decrypted_message}")

ngram = Ngram('english_2grams.csv', ',')

def mutate_grill_key(n, key):
    import copy

    center = n // 2
    # Zbiór aktualnie zajętych pól (uwzględniając wszystkie rotacje)
    used = set()
    for x, y in key:
        for r in range(4):
            used.add(rotate_coords(n, x, y, r))

    # Wybierz losową pozycję z aktualnego klucza
    new_key = copy.deepcopy(key)
    idx_to_replace = random.randrange(len(new_key))
    old_pos = new_key[idx_to_replace]

    # Usuń stare rotacje z użytych
    for r in range(4):
        used.remove(rotate_coords(n, old_pos[0], old_pos[1], r))

    # Próbuj znaleźć nową pozycję, która nie koliduje
    attempts = 0
    while attempts < 1000:
        x, y = random.randint(0, n-1), random.randint(0, n-1)
        if (x, y) == (center, center):
            continue
        new_group = set(rotate_coords(n, x, y, r) for r in range(4))
        if not new_group & used:
            new_key[idx_to_replace] = (x, y)
            return new_key
        attempts += 1

    # Jeśli nie udało się znaleźć lepszej mutacji, zwróć niezmieniony klucz
    print("KEY", key)
    return key

# def mutate_grill_key(n, key):
#     import copy
#
#     center = n // 2
#     new_key = copy.deepcopy(key)
#
#     # Zbiór aktualnie zajętych pól (uwzględniając wszystkie rotacje)
#     def all_rotated_positions(key_list):
#         pos_set = set()
#         for x, y in key_list:
#             for r in range(4):
#                 pos_set.add(rotate_coords(n, x, y, r))
#         return pos_set
#
#     # Wybierz dwie różne losowe pozycje do zastąpienia
#     if len(new_key) < 2:
#         return key  # nie da się mutować dwóch, jeśli mniej niż 2
#     idx1, idx2 = random.sample(range(len(new_key)), 2)
#     old_pos1, old_pos2 = new_key[idx1], new_key[idx2]
#
#     # Usuń ich rotacje z zajętych pól
#     temp_key = copy.deepcopy(new_key)
#     del temp_key[max(idx1, idx2)]
#     del temp_key[min(idx1, idx2)]
#     used = all_rotated_positions(temp_key)
#
#     attempts = 0
#     found = False
#     while attempts < 1000:
#         x1, y1 = random.randint(0, n-1), random.randint(0, n-1)
#         x2, y2 = random.randint(0, n-1), random.randint(0, n-1)
#         if (x1, y1) == (center, center) or (x2, y2) == (center, center):
#             attempts += 1
#             continue
#
#         group1 = set(rotate_coords(n, x1, y1, r) for r in range(4))
#         group2 = set(rotate_coords(n, x2, y2, r) for r in range(4))
#
#         # Sprawdź, czy nowe pozycje nie kolidują między sobą ani z resztą
#         if not (group1 & used or group2 & used or group1 & group2):
#             new_key[idx1] = (x1, y1)
#             new_key[idx2] = (x2, y2)
#             found = True
#             break
#
#         attempts += 1
#
#     return new_key if found else key


def shotgun_hill_climbing_for_grill(C, ngram_model, n, timelimit=10, wait_to_progress=0.1):
    def score(key):
        decrypted = decrypt_with_grill_verbose(n, C, key).lower()
        return ngram_model.score(decrypted)

    best_key = generate_random_grill_key(n)
    best_score = score(best_key)
    best_decryption = decrypt_with_grill_verbose(n, C, best_key)

    t0 = time.time()
    iteration = 0
    start_time = time.time()

    print("🚀 Start ataku wspinaczkowego (Shotgun Hill Climbing)...")
    print(f"🔐 Początkowy klucz: {best_key}")
    print(f"📊 Początkowy score: {best_score:.4f}")
    print(f"📜 Początkowy dekrypt (fragment): {best_decryption[:80]}...\n")

    while time.time() - t0 < timelimit:
        iteration += 1
        current_key = generate_random_grill_key(n)
        current_score = score(current_key)
        time_progress = time.time()
        current_decryption = decrypt_with_grill_verbose(n, C, current_key)
        #
        # print(f"\n🔁 Iteracja {iteration}:")
        # print(f"  ⏱️ Czas od startu: {time.time() - t0:.2f}s")
        # print(f"  🎲 Startowy score: {current_score:.4f}")
        # print(f"  📜 Startowy dekrypt (fragment): {current_decryption[:80]}...\n")

        while time.time() - time_progress < wait_to_progress:
            new_key = mutate_grill_key(n, current_key)
            new_decryption = decrypt_with_grill_verbose(n, C, new_key).lower()
            new_score = ngram_model.score(new_decryption)

            # print(f"NEWSCORE {new_score} vs CURRENTSCORE {current_score}")
            # print(new_score > current_score)

            # print(new_key)

            if new_score > current_score:
                current_key = new_key
                current_score = new_score
                current_decryption = new_decryption
                time_progress = time.time()

                print(f"    ✅ Lepszy lokalny wynik! Aktualny score: {current_score:.4f} oraz tekst: {current_decryption[:80]}... Best wynik: {best_score} oraz tekst: {best_decryption[:80]}")

                if new_score > best_score:
                    best_key = new_key
                    best_score = new_score
                    best_decryption = new_decryption

                    t0 = time.time()

                    print("    💡 Nowy NAJLEPSZY wynik GLOBALLY!")
                    print(f"    🔑 Klucz: {best_key}")
                    print(f"    📜 Dekrypt (fragment): {best_decryption[:80]}...\n")

    print("\n🏁 Koniec ataku.")
    print(f"✅ Najlepszy wynik końcowy: {best_score:.4f}")
    print(f"🔑 Klucz: {best_key}")
    print(f"📜 Dekrypt: {best_decryption[:200]}...\n")
    print(f"📜 Czas: {(time.time() - start_time) / 60:.2f}m {(time.time() - start_time) % 60:.2f}s...\n")

    if message:
        matches = sum(1 for a, b in zip(best_decryption.lower(), message.lower()) if a == b)
        total = len(message)
        accuracy = (matches / total) * 100
        print(f"📊 Zgodność z oryginałem: {matches}/{total} znaków ({accuracy:.2f}%)")

    return best_score, best_key, best_decryption

#
# Zakładamy, że 'encrypted_message' już istnieje i ngram został załadowany jako 'ngram'
score, found_key, cracked_message = shotgun_hill_climbing_for_grill(
    encrypted_message,
    ngram_model=ngram,
    n=n,
    timelimit=600,  # np. 30 sekund
    wait_to_progress=20
)

print("\n📌 Ostateczny wynik:")
print("🔑 Klucz original:", key)
print("🔑 Klucz:", found_key)
print("🔑 Wynik:", score)
print("📜 Oryginalna wiadomość:", message.lower())
print("📜 Odszyfrowana wiadomość:", cracked_message)
