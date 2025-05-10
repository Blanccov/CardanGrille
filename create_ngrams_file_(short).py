alfabet='abcdefghijklmnopqrstuvwxyz'
with open('book6.txt', encoding='utf-8') as f:
    book = f.read()
book2 = ''.join( [x for x in book if x.isalpha() and x in alfabet ] ).lower()
dct, srt = {}, []
for bigram in [ a+b for a in alfabet for b in alfabet ]:
    dct[ bigram ] = 0
for i in range( len( book2)-2 ):
    dct[ book2[i:i+2] ] += 1
for k in dct.keys():
    srt.append( (dct[k],k) )
srt.sort(reverse=True)
with open('my_english_bigrams.txt', 'w', encoding='utf-8') as f:
    for elem in srt: f.write( elem[1] + ' ' + str( elem[0] ) + '\n' )
