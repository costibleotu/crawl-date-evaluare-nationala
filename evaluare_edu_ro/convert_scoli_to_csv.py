import csv
import json
from glob import glob
csv_header = ['cod','nume','tip','judet','sector','adresa','e_mail','mediu','telefon','fax','an','nr_nerepartizati','nr_candidati','nr_repartizati']
for file in glob('data/scoli_*.json'):
  print(file)
  with open(file, 'r') as json_file:
    json_data = json.load(json_file)
    with open(file.replace('json', 'csv'), 'w') as csvfile:
        csv_scoala = csv.writer(csvfile, delimiter=';',
                            quotechar='"', quoting=csv.QUOTE_ALL)
        csv_scoala.writerow(csv_header)
        for scoala in json_data:
            row = []
            for k in csv_header:
                row.append(scoala[k])
            else:
                csv_scoala.writerow(row)
