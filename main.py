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

    for rot in range(4):
        print(f"🌀 Rotacja {rot * 90}°:")
        print_key_grid(n, key_positions, rot)  # Wizualizacja klucza
        for i, (x, y) in enumerate(key_positions):
            rx, ry = rotate_coords(n, x, y, rot)
            if (rx, ry) == (n//2, n//2):
                continue
            grid[rx][ry] = message[msg_idx]
            print(f"  Wpisuję '{message[msg_idx]}' → pole ({rx},{ry})")
            msg_idx += 1
        print_grid(grid)
    return grid

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
encrypted_grid = encrypt_with_grill_verbose(n, message, key)
