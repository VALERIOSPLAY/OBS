


def batcher_exec(file, func, batch_size=1000):
    batch = []
    for i, line in enumerate(tqdm.tqdm(file), start=1):

        batch.append(line)
        if i % batch_size == 0 or line == '':
            processed_batch = list(map(func, batch))
