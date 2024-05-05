import json
import csv
import tqdm



batch_size = 10

def to_row(raw_line):
    try:
        ln = raw_line[59:]
        wln = [json.loads(ln)["title"], json.loads(ln)["authors"][0]["author"]["key"], json.loads(ln)["created"]["value"]]
        return wln
    except Exception as e:
        return []


with open("D:\\BookScan\\ol_dump_works_2024-01-31.txt", encoding='utf-8') as f, open('works.csv', 'w', newline='', encoding="utf-8") as file:

    batch = []
    writer = csv.writer(file)
    for i, line in enumerate(tqdm.tqdm(f), start=1):

        batch.append(line)
        if i % batch_size == 0 or line == '':
            processed_batch = list(map(to_row, batch))
            writer.writerows(processed_batch)
            batch = []





