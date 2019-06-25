import csv
from pprint import pprint

final = {}
with open('data/evaluare_extra_2019.csv') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    for row in reader:
        url = row['url'].split('=')[-1]
        final.setdefault(url, 0)
        final[url] += 1
pprint(final)

for i in range(1, 698):
    if not final.get(str(i), ''):
        print('{} not found'.format(i))
