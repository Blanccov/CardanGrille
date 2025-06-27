import os

alfabet = 'AÀBCÇDEÈÉFGHIÍÏJKLMNOÒÓPQRSTUÚÜVWXYZ'

folder_path = './books'

combined_text = ''
for filename in os.listdir(folder_path):
    if filename.endswith('.txt'):
        with open(os.path.join(folder_path, filename), encoding='utf-8') as f:
            combined_text += f.read()

book2 = ''.join([c for c in combined_text.upper() if c in alfabet])

dct = {a + b: 0 for a in alfabet for b in alfabet}

for i in range(len(book2) - 1):
    bigram = book2[i:i+2]
    if bigram in dct:
        dct[bigram] += 1

srt = sorted(dct.items(), key=lambda x: x[1], reverse=True)

with open('my_catalan_bigrams.csv', 'w', encoding='utf-8') as f:
    for bigram, count in srt:
        if count > 0:
            f.write(f"{bigram} {count}\n")