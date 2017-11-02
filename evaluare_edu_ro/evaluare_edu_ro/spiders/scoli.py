# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
from bs4 import BeautifulSoup as soup
import re
from evaluare_edu_ro.items import ScoalaItem
import base64


county_map = {
    1: "ALBA",
    2: "ARGES",
    3: "ARAD",
    5: "BACAU",
    6: "BIHOR",
    7: "BISTRITA-NASAUD",
    8: "BRAILA",
    10: "BRASOV",
    9: "BOTOSANI",
    11: "BUZAU",
    12: "CLUJ",
    13: "CALARASI",
    14: "CARAS-SEVERIN",
    15: "CONSTANTA",
    16: "COVASNA",
    17: "DAMBOVITA",
    18: "DOLJ",
    19: "GORJ",
    20: "GALATI",
    21: "GIURGIU",
    22: "HUNEDOARA",
    23: "HARGHITA",
    25: "IALOMITA",
    26: "IASI",
    27: "MEHEDINTI",
    28: "MARAMURES",
    29: "MURES",
    30: "NEAMT",
    31: "OLT",
    32: "PRAHOVA",
    33: "SIBIU",
    34: "SALAJ",
    35: "SATU-MARE",
    36: "SUCEAVA",
    37: "TULCEA",
    38: "TIMIS",
    39: "TELEORMAN",
    40: "VALCEA",
    41: "VRANCEA",
    42: "VASLUI",
    24: "ILFOV",
    4: "BUCURESTI",
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

class ScoliSpider(scrapy.Spider):
    name = 'scoli'
    allowed_domains = ['admitere.edu.ro', 'cloudapp.net']
    start_urls = []

    def __init__(self, year=None):
        if year:
            self.year = int(year)
        else:
            self.year = datetime.now().year



    def start_requests(self):
        if self.year == 2017:
            for county_i, county_name in county_map.items():
                url = 'http://admitere.edu.ro/Pages/Scoli.aspx?jud={}'.format(county_i)
                yield scrapy.Request(
                    url=url,
                    callback=self.parse_scoli_new,
                    meta={'county': county_name, 'county_i': county_i, 'url': url})

        elif self.year == 2016:
            for county_i, county_name in county_map.items():
                url = 'http://repartizare1.cloudapp.net/Pages/Scoli.aspx?jud={}'.format(county_i)
                yield scrapy.Request(
                    url=url,
                    callback=self.parse_scoli_new,
                    meta={'county': county_name, 'county_i': county_i, 'url': url})
        elif self.year in range(2004,2016):
            for county_i, county_name in county_map_acro.items():
                url = 'http://static.admitere.edu.ro/{}/staticRepI/j/{}/sc/page_1.html'.format(self.year, county_i)
                yield scrapy.Request(
                    url=url,
                    callback=self.parse_scoli,
                    meta={'county': county_name, 'county_i': county_i, 'current_page': 1})



    def parse_scoli_new(self, response):
        root = soup(response.body, 'html.parser')
        county = response.meta['county']
        county_i = response.meta['county_i']
        url = response.meta['url']

        # select_page = root.find('select', attrs={'name': 'ctl00$ContentPlaceHolderBody$DropDownList2'})
        tabel = root.find('table', {'class': 'mainTable'})
        if tabel:
            for scoala in tabel.find_all('tr')[1:]:
                td_scoala = scoala.find_all('td')
                item = ScoalaItem()
                item['an'] = self.year
                item['judet'] = county
                item['cod'] = td_scoala[1].text
                item['nume'] = td_scoala[2].text
                item['nr_candidati'] = td_scoala[3].text
                item['nr_repartizati'] = td_scoala[4].text
                item['nr_nerepartizati'] = td_scoala[5].text
                item['tip'] = td_scoala[6].text
                item['mediu'] = td_scoala[7].text
                item['adresa'] = td_scoala[8].text
                item['sector'] = td_scoala[9].text
                item['telefon'] = td_scoala[10].text
                item['fax'] = td_scoala[11].text
                item['e_mail'] = td_scoala[12].text
                yield item
            viewstate = root.find('input', attrs={'name': '__VIEWSTATE'})['value']
            viewstategen = root.find('input', attrs={'name': '__VIEWSTATEGENERATOR'})['value']
            eventvalidation = root.find('input', attrs={'name': '__EVENTVALIDATION'})['value']

            yield scrapy.http.FormRequest(url=url,
                        formdata={
                            'ctl00$ContentPlaceHolderBody$ImageButtonDR1.x': '18',
                            'ctl00$ContentPlaceHolderBody$ImageButtonDR1.y': '10',
                            '__VIEWSTATE': viewstate,
                            '__VIEWSTATEGENERATOR': viewstategen,
                            '__EVENTVALIDATION': eventvalidation
                            },
                        callback=self.parse_scoli_new,
                        meta={'county': county, 'county_i': county_i, 'url': url})




    def parse_scoli(self, response):
        root = soup(response.body, 'html.parser')
        county = response.meta['county']
        county_i = response.meta['county_i']
        current_page = response.meta['current_page']
        if self.year in [2010]:
            regex = r'^.*ged\(\){return \"(.*)\";}'
            ged = re.findall(regex, root.find('script').text)[0]
            dec_ged = base64.b64decode(s3(ged))
            root = soup(dec_ged, 'html.parser')
        # select_page = root.find('select', attrs={'name': 'ctl00$ContentPlaceHolderBody$DropDownList2'})
        tabel = root.find('table', {'class': 'mainTable'})
        for scoala in tabel.find_all('tr')[1:]:
            td_scoala = scoala.find_all('td')
            item = ScoalaItem()
            item['an'] = self.year
            item['judet'] = county
            item['cod'] = td_scoala[1].text.replace('\u00a0','')
            item['nume'] = td_scoala[2].text.replace('\u00a0','')
            item['nr_candidati'] = td_scoala[3].text.replace('\u00a0','')
            item['nr_repartizati'] = td_scoala[4].text.replace('\u00a0','')
            item['nr_nerepartizati'] = td_scoala[5].text.replace('\u00a0','')
            item['tip'] = td_scoala[6].text.replace('\u00a0','')
            item['mediu'] = td_scoala[7].text.replace('\u00a0','')
            item['adresa'] = td_scoala[8].text.replace('\u00a0','')
            item['sector'] = td_scoala[9].text.replace('\u00a0','')
            item['telefon'] = td_scoala[10].text.replace('\u00a0','')
            item['fax'] = td_scoala[11].text.replace('\u00a0','')
            item['e_mail'] = td_scoala[12].text.replace('\u00a0','')

            yield item


        first_script = root.find('script').text
        regex = r".*noOfPages=(\d+)"
        no_of_pages = int(re.findall(regex, first_script)[0])
        if current_page < no_of_pages:
            next_url = 'http://static.admitere.edu.ro/{}/staticRepI/j/{}/sc/page_{}.html'.format(self.year, county_i, current_page+1)
            yield scrapy.Request(
                url=next_url,
                callback=self.parse_scoli,
                meta={'county': county, 'county_i': county_i, 'current_page': current_page+1})



def str_replace(srch, rplc, sbjct):
    if len(sbjct) == 0:
        return ''

    if len(srch) == 1:
        return sbjct.replace(srch[0], rplc[0])

    lst = sbjct.split(srch[0])
    reslst = []
    for s in lst:
        reslst.append(str_replace(s, srch[1:], rplc[1:]))
    return rplc[0].join(reslst)


def s0(a, b, c):
    a = str_replace(b, '_', a)
    a = str_replace(c, b, a)
    a = str_replace('_', c, a)
    return a


def s1(a, b):
    return s0(a, b.lower(), b.upper())


def s2(a):
    for i in ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]:
        a = s1(a, i)
    return a


def s3(a):
    a = s0(a, "0", "O")
    a = s0(a, "1", "l")
    a = s0(a, "5", "S")
    a = s0(a, "m", "s")
    a = s2(a)

    return a