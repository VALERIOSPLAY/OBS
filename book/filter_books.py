import csv
import tqdm
import cd
import time


batch_size = 100000
dct = cd.CompressedDict()
ad = dict()

with open("D:\\BookScan\\authors.csv", newline='', encoding='utf-8') as a:
    reader = csv.reader(a, delimiter=',')
    for i in reader:
        try:
            ad[i[1]] = i[0]
        except Exception as e:
            pass
    print('table formed')

def sortfunc(batch):
    processed_batch = []
    for i in batch:
        if len(i) == 3:
            try:
                processed_batch.append((ad[i[1]],i[0]))
            except Exception as e:
                pass
    dct.update_values(processed_batch)


with open("D:\\BookScan\\works.csv", newline='', encoding='utf-8') as w, open("out1.txt", 'wt', newline='', encoding='utf-8') as o:

    start_time = time.time()
    batch = []
    wtbl = csv.reader(w, delimiter=',')
    for i, line in enumerate(tqdm.tqdm(wtbl, desc='books filtered'), start=1):
        
        batch.append(line)
        if i % batch_size == 0 or line == '':
            sortfunc(batch)
            batch = []
    for i in dct.dict_files:
        dct_part = dct.load_dict(i)
        for i in dct_part.items():
            o.write(str(i)+'\n')
    for i in dct.current_dict.items():
        o.write(str(i) + '\n')

    end_time = time.time()
    print(f'estimated: {end_time - start_time}')
