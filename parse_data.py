import json
import os
from ustav import html_to_cslavonic

def read_json(fname):
    with open(fname, 'r', encoding='utf-8') as f:
        return json.load(f)

def dump_text(base, text):
    os.makedirs(base, exist_ok=True)
    with open(f'{base}/index.xml', 'w') as f:
        f.write(html_to_cslavonic(text))

def dump_book(base, book):
    toc = []
    for i,chap in enumerate(book):
        name = chap['name']
        key = f'{i+1:04d}'
        toc.append({'name': name, 'key': key})

        if 'text' not in chap:
            if 'general' in chap:
                dump_text(f'{base}/{key}', chap['general'])
            loca = list(chap.keys() - {'name', 'general'})
            if len(loca) != 1:
                import pdb; pdb.set_trace()
            assert len(loca) == 1, loca
            loca = loca[0]
            dump_book(f'{base}/{key}', chap[loca])
        else:
            dump_text(f'{base}/{key}', chap['text'])

    with open(base + '/index.json', 'w') as f:
        json.dump(toc, f, ensure_ascii=False, indent=4)


### Evangelie
# TODO


### Apostol
# TODO

### Chasoslov
toc = ["Вечерня", "Павечерница великая", "Павечерница средняя", "Павечерница малая", "Полунощница повседневная", "Полунощница субботняя", "Полунощница воскресная", "Утреня", "Час первый", "Час третий", "Час шестой", "Час девятый", "Псалмы на литургии", "Тропари воскресны и Богородичны", "Тропари и кондаки дневные", "Богородичны и крестобогородичны", "Тропари Четверодесятницы", "Тропари пятидесятницы"]
data = read_json('data/chasoslov.json')
assert len(toc) == len(data)
chasoslov = []
for name, key in zip(toc, data.keys()):
    assert len(data[key]) == 1
    assert len(data[key][0]) == 1
    chasoslov.append({
        'name': name,
        'text': data[key][0]['text'],
    })
dump_book('books/chasoslov', chasoslov)


### Psaltyr
data = read_json('data/psaltyr.json')
dump_book('books/psaltyr', data)


### Kanonnik
data = read_json('data/kanonnik.json')
dump_book('books/kanonnik', data)


### Pravilnye kanony FIXME: inner structure not understood
data = read_json('data/pravilnye-kanony.json')
assert len(data) == 1
dump_text('books/pravilnye-kanony', data['general'])

### Prichastnye chasy
data = read_json('data/prichastnye-chasy.json')
dump_book('books/prichastnye-chasy', data)

### Pogrebenie
data = read_json('data/pogrebenie.json')
dump_book('books/pogrebenie', data)
