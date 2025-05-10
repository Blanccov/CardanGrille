import random

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

    print("🔓 Proces deszyfrowania:")

    decrypted_message = ""

    # Odczytujemy litery z grida na podstawie rotacji klucza
    for rot in range(4):
        print(f"🌀 Rotacja {rot * 90}°:")

        # Rotujemy współrzędne klucza
        rotated_key_positions = [rotate_coords(n, x, y, rot) for x, y in key_positions]
        rotated_key_positions.sort()

        # Wizualizacja grida i klucza
        print_key_grid(n, key_positions, rot)  # Wizualizacja klucza
        print_grid(decrypt_grid)  # Można pokazać grid po wszystkich rotacjach

        # Odczytujemy wiadomość, korzystając z otworów w kluczu
        for x, y in rotated_key_positions:
            if (x, y) == (n // 2, n // 2):
                continue  # Ignorujemy środek
            decrypted_message += grid[x][y]
            decrypt_grid[x][y] = '.'
            print(f"  Odczytuję '{grid[x][y]}' → pole ({x},{y})")

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
n = 5  # Można ustawić na dowolną liczbę nieparzystą
message = "WiadomośćDoSzyfrowaniaJestBanalnieIdealnaTadeuszu"  # Można podać dowolną wiadomość

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
