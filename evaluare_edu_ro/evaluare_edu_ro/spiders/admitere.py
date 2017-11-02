# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
from bs4 import BeautifulSoup as soup
import re
from evaluare_edu_ro.items import AdmitereEduRoItem
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

class AdmitereSpider(scrapy.Spider):
    name = 'admitere'
    allowed_domains = ['admitere.edu.ro', 'cloudapp.net']
    start_urls = []

    def __init__(self, year=None):
        if year:
            self.year = int(year)
        else:
            self.year = datetime.now().year



    def start_requests(self):
        print(self.year)
        if self.year == 2017:
            for county_i, county_name in county_map.items():
                url = 'http://admitere.edu.ro/Pages/CandFromJud.aspx?jud={0}&JudProv={0}&alfa=2'.format(county_i)
                yield scrapy.Request(
                    url=url,
                    callback=self.parse_new,
                    meta={'county': county_name, 'county_i': county_i, 'url': url})

        elif self.year == 2016:
            for county_i, county_name in county_map.items():
                url = 'http://repartizare1.cloudapp.net/Pages/CandFromJud.aspx?jud={0}&JudProv={0}&alfa=2'.format(county_i)
                yield scrapy.Request(
                    url=url,
                    callback=self.parse_new,
                    meta={'county': county_name, 'county_i': county_i, 'url': url})
        elif self.year in range(2004,2016):
            for county_i, county_name in county_map_acro.items():
                url = 'http://static.admitere.edu.ro/{}/staticRepI/j/{}/couta/page_1.html'.format(self.year, county_i)
                yield scrapy.Request(
                    url=url,
                    callback=self.parse,
                    meta={'county': county_name, 'county_i': county_i, 'current_page': 1})

    def parse_new(self, response):
        root = soup(response.body, 'html.parser')
        county = response.meta['county']
        county_i = response.meta['county_i']
        url = response.meta['url']

        # select_page = root.find('select', attrs={'name': 'ctl00$ContentPlaceHolderBody$DropDownList2'})
        tabel = root.find('table', {'class': 'mainTable'})
        for elev in tabel.find_all('tr')[1:]:
            td_elev = elev.find_all('td')

            item = AdmitereEduRoItem()
            item['nume'] = td_elev[1].text
            item['scoala_de_provenienta'] = td_elev[2].text
            item['judet'] = td_elev[3].text
            item['media_la_admitere'] = td_elev[4].text
            item['media_en_tsu'] = td_elev[5].text
            item['media_de_absolvire'] = td_elev[6].text
            item['nota_lb_romana'] = td_elev[7].text
            item['nota_matematica'] = td_elev[8].text
            item['optiunea_3'] = td_elev[9].text
            item['nota_optiunea_3'] = td_elev[10].text
            item['limba_materna'] = td_elev[11].text
            item['nota_lb_materna'] = td_elev[12].text
            try:
                item['liceu_repartizat'] = td_elev[13].find('a').text
                item['tip_liceu'] = td_elev[13].find('font').text
                item['specializare'] = td_elev[14].find('a').text
                item['specializare_lb'] = td_elev[14].find('font').text
            except:
                pass
            yield item

        viewstate = root.find('input', attrs={'name': '__VIEWSTATE'})['value']
        viewstategen = root.find('input', attrs={'name': '__VIEWSTATEGENERATOR'})['value']
        eventvalidation = root.find('input', attrs={'name': '__EVENTVALIDATION'})['value']

        yield scrapy.http.FormRequest(url=url,
                    formdata={
                        # 'ctl00$ContentPlaceHolderBody$DropDownList2:': str(current_page), 
                        'ctl00$ContentPlaceHolderBody$ImageButtonDR1.x': '18',
                        'ctl00$ContentPlaceHolderBody$ImageButtonDR1.y': '10',
                        '__VIEWSTATE': viewstate,
                        '__VIEWSTATEGENERATOR': viewstategen,
                        '__EVENTVALIDATION': eventvalidation
                        },
                    callback=self.parse_new,
                    meta={'county': county, 'county_i': county_i, 'url': url})


    def parse(self, response):
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
        for elev in tabel.find_all('tr')[1:]:
            td_elev = elev.find_all('td')

            item = AdmitereEduRoItem()
            item['nume'] = td_elev[1].text
            item['scoala_de_provenienta'] = td_elev[2].text
            item['judet'] = td_elev[3].text
            item['media_la_admitere'] = td_elev[4].text
            item['media_en_tsu'] = td_elev[5].text
            item['media_de_absolvire'] = td_elev[6].text
            item['nota_lb_romana'] = td_elev[7].text
            item['nota_matematica'] = td_elev[8].text
            item['optiunea_3'] = td_elev[9].text
            item['nota_optiunea_3'] = td_elev[10].text
            item['limba_materna'] = td_elev[11].text
            item['nota_lb_materna'] = td_elev[12].text
            try:
                item['liceu_repartizat'] = td_elev[13].find('a').text
                item['tip_liceu'] = td_elev[13].find('font').text
                item['specializare'] = td_elev[14].find('a').text
                item['specializare_lb'] = td_elev[14].find('font').text
            except:
                pass
            yield item
        first_script = root.find('script').text
        regex = r".*noOfPages=(\d+)"
        no_of_pages = int(re.findall(regex, first_script)[0])
        if current_page < no_of_pages:
            next_url = 'http://static.admitere.edu.ro/{}/staticRepI/j/{}/couta/page_{}.html'.format(self.year, county_i, current_page+1)
            yield scrapy.Request(
                url=next_url,
                callback=self.parse,
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