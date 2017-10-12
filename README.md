# crawl-date-evaluare-nationala

Students results for National Evaluation (Romania) - years 2015-2017


## Environemnt setup
```bash
mkvirtualenv --python=python3 <virtualenv_name>
pip install -r requirements.txt
```

## Run crawler
```bash
scrapy crawl evaluare -a year=2016 -o evaluare_2016.csv
```

### Spider arguments
`year` (optional) - any available year(from 2015 to present). If not specified it will take current year  


## Contribution
Feel free to contribute to this repo or give feedback. For more info contact me at [costin.bleotu@databus.systems](mailto:costin.bleotu@databus.systems).