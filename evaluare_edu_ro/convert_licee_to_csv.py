import csv
import json
from glob import glob
csv_header = ['tip','nume','cod_liceu','telefon','an','sectorul','fax']
empty_list = ['','','','','','']
specializari_header = ['candidati_repartizati','cod','limba_predare','filiera','denumire','nivel','nr_locuri','profil','ultima_medie','forma_invatamant','mediul','ultima_medie_precedenta','bilingv']
for file in glob('data/licee_2017.json'):
  print(file)
  with open(file, 'r') as json_file:
    json_data = json.load(json_file)
    # print(json_data)
    header = []
    header = json_data[0].keys()
    with open(file.replace('json', 'csv'), 'w') as csvfile:
        csv_liceu = csv.writer(csvfile, delimiter=';',
                            quotechar='"', quoting=csv.QUOTE_ALL)
        csv_liceu.writerow(csv_header + ['specializare_' + x for x in specializari_header])
        for liceu in json_data:
            base_row = []
            for k in csv_header:
                base_row.append(liceu[k])
            if liceu['specializari']:
                prima_specializare = True
                for specializare in liceu['specializari']:
                    row = []
                    for kk in specializari_header:
                        row.append(specializare[kk])
                    if prima_specializare:
                        csv_liceu.writerow(base_row + row)
                    else:
                        csv_liceu.writerow(empty_list + row)
                    prima_specializare = False
            else:
                csv_liceu.writerow(base_row)
