# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
from bs4 import BeautifulSoup as soup
import re
from evaluare_edu_ro.items import EvaluareEduRoItem
import base64
import requests

county_map = {
    # 1: "ALBA",
    # 2: "ARGES",
    # 3: "ARAD",
    4: "BUCURESTI",
    # 5: "BACAU",
    # 6: "BIHOR",
    # 7: "BISTRITA-NASAUD",
    # 8: "BRAILA",
    # 9: "BOTOSANI",
    # 10: "BRASOV",
    # 11: "BUZAU",
    # 12: "CLUJ",
    # 13: "CALARASI",
    # 14: "CARAS-SEVERIN",
    # 15: "CONSTANTA",
    # 16: "COVASNA",
    # 17: "DAMBOVITA",
    # 18: "DOLJ",
    # 19: "GORJ",
    # 20: "GALATI",
    # 21: "GIURGIU",
    # 22: "HUNEDOARA",
    # 23: "HARGHITA",
    # 24: "ILFOV",
    # 25: "IALOMITA",
    # 26: "IASI",
    # 27: "MEHEDINTI",
    # 28: "MARAMURES",
    # 29: "MURES",
    # 30: "NEAMT",
    # 31: "OLT",
    # 32: "PRAHOVA",
    # 33: "SIBIU",
    # 34: "SALAJ",
    # 35: "SATU-MARE",
    # 36: "SUCEAVA",
    # 37: "TULCEA",
    # 38: "TIMIS",
    # 39: "TELEORMAN",
    # 40: "VALCEA",
    # 41: "VRANCEA",
    # 42: "VASLUI",
}

county_map_acro = {
    "AB": "ALBA",
    "AG": "ARGES",
    "AR": "ARAD",
    "BC": "BACAU",
    "BH": "BIHOR",
    "BN": "BISTRITA-NASAUD",
    "BR": "BRAILA",
    "BV": "BRASOV",
    "BT": "BOTOSANI",
    "BZ": "BUZAU",
    "CJ": "CLUJ",
    "CL": "CALARASI",
    "CS": "CARAS-SEVERIN",
    "CT": "CONSTANTA",
    "CV": "COVASNA",
    "DB": "DAMBOVITA",
    "DJ": "DOLJ",
    "GJ": "GORJ",
    "GL": "GALATI",
    "GR": "GIURGIU",
    "HD": "HUNEDOARA",
    "HR": "HARGHITA",
    "IL": "IALOMITA",
    "IS": "IASI",
    "MH": "MEHEDINTI",
    "MM": "MARAMURES",
    "MS": "MURES",
    "NT": "NEAMT",
    "OT": "OLT",
    "PH": "PRAHOVA",
    "SB": "SIBIU",
    "SJ": "SALAJ",
    "SM": "SATU-MARE",
    "SV": "SUCEAVA",
    "TL": "TULCEA",
    "TM": "TIMIS",
    "TR": "TELEORMAN",
    "VL": "VALCEA",
    "VN": "VRANCEA",
    "VS": "VASLUI",
    "IF": "ILFOV",
    "B": "BUCURESTI"
}

class EvaluareSpider(scrapy.Spider):
    name = 'evaluare'
    allowed_domains = ['evaluare.edu.ro']
    start_urls = []
    errors = {}
    def __init__(self, year=None):
        if year:
            self.year = int(year)
        else:
            self.year = datetime.now().year



    def start_requests(self):

        if self.year == 2019:
            for county_i, county_name in county_map.items():
                url = 'http://evaluare.edu.ro/Evaluare/CandFromJudAlfa.aspx?Jud={}&PageN=1'.format(county_i)
                response = requests.get(url)
                root = soup(response.text, 'html.parser')

                select = root.find('select', {'name': 'ctl00$ContentPlaceHolderBody$DropDownList2'})
                num_pages = select.find_all('option')[-1].attrs['value']
                print('Found {} pages for {}'.format(num_pages, county_name))
                print('----')
                # for i in [303, 631, 679]:
                for i in range(1,int(num_pages) + 1):
                #     # print(i)
                # # if not stop_crawl:
                #     # next_page = root.find('input', attrs={'title': 'Pagina următoare'})
                    next_url = 'http://evaluare.edu.ro/Evaluare/CandFromJudAlfa.aspx?Jud={}&PageN={}'.format(county_i, i)
                #     # if current_page < 5:
                    yield scrapy.Request(
                        url=next_url,
                        callback=self.parse,
                        meta={'county': county_name, 'county_i': county_i, 'current_page': i})
                # yield scrapy.Request(
                #     url=url,
                #     callback=self.parse,
                #     meta={'county': county_name, 'county_i': county_i, 'current_page': 1})
        else:
            for county_i, county_name in county_map_acro.items():
                url = 'http://static.evaluare.edu.ro/{}/rapoarte/j/{}/cand/a/page_1.html'.format(self.year, county_i)
                yield scrapy.Request(
                    url=url,
                    callback=self.parse,
                    meta={'county': county_name, 'county_i': county_i, 'current_page': 1})

    def parse(self, response):
        root = soup(response.body, 'html.parser')

        county_i = response.meta['county_i']
        county = response.meta['county']
        current_page = response.meta['current_page']
        recrawl = response.meta.get('recrawl', False)
        if recrawl:
            print('---Crawling page {} from {}'.format(current_page, county))
        else:
            print('Crawling page {} from {}'.format(current_page, county))
        tabel = root.find('table', {'class': 'mainTable'})
        # stop_crawl = True if len(tabel.find_all('tr')) == 2 else False
        try:
            for elev in tabel.find_all('tr')[2:]:
                td_elev = elev.find_all('td')
                item = EvaluareEduRoItem()
                item['an'] = self.year
                item['judet'] = county
                item['nume'] = td_elev[1].text
                item['url'] = response.url
                item['pozitia_pe_tara'] = td_elev[2].text
                item['unitate_de_invatamant'] = td_elev[3].text
                item['lb_romana_nota'] = td_elev[4].text
                item['lb_romana_contestatie'] = td_elev[5].text
                item['lb_romana_final'] = td_elev[6].text
                item['matematica_nota'] = td_elev[7].text
                item['matematica_contestatie'] = td_elev[8].text
                item['matematica_final'] = td_elev[9].text
                item['lb_materna'] = td_elev[10].text
                item['lb_materna_nota'] = td_elev[11].text
                item['lb_materna_contestatie'] = td_elev[12].text
                item['lb_materna_final'] = td_elev[13].text
                item['media'] = td_elev[14].text
                yield item
        except Exception as e:
            print(e)
            crawled = False
            self.errors.setdefault(county, {})
            self.errors[county].setdefault(current_page, 0)
            self.errors[county][current_page] += 1
            if self.errors[county][current_page] < 3:
                print('--Retring crawling page {} from {} [{} time]'.format(current_page, county, self.errors[county][current_page]))
                next_url = 'http://evaluare.edu.ro/Evaluare/CandFromJudAlfa.aspx?Jud={}&PageN={}'.format(county_i, current_page)
                yield scrapy.Request(
                        url=next_url,
                        callback=self.parse,
                        meta={'county': county, 'county_i': county_i, 'current_page': current_page, 'recrawl': True})
                print('YELD sent')
        # if self.year == 2019:
            
        # else:
        #     first_script = root.find('script').text
        #     regex = r".*noOfPages=(\d+)"
        #     no_of_pages = int(re.findall(regex, first_script)[0])
        #     if current_page < no_of_pages:
        #         next_url = 'http://static.evaluare.edu.ro/{}/rapoarte/j/{}/cand/a/page_{}.html'.format(self.year, county_i, current_page+1)
        #         yield scrapy.Request(
        #             url=next_url,
        #             callback=self.parse,
        #             meta={'county': county, 'county_i': county_i, 'current_page': current_page+1})
