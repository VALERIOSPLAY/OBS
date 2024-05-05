import json
import csv
import tqdm


batch_size = 100

def to_row(raw_line):
    try:
        ln = '{'+raw_line.split('{', 1)[1]
        wln = [json.loads(ln)["name"], json.loads(ln)["key"]]
        return wln
    except Exception as e:
        return []

with open("D:\\BookScan\\ol_dump_authors_2024-02-29.txt", encoding='utf-8') as f, open("authors.csv", 'wt', newline='', encoding='utf-8') as file:

    batch = []
    writer = csv.writer(file)
    for i, line in enumerate(tqdm.tqdm(f), start=1):
        batch.append(line)
        if i % batch_size == 0 or line == '':
            processed_batch = list(map(to_row, batch))
            writer.writerows(processed_batch)
            batch = []

