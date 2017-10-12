# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class EvaluareEduRoItem(Item):
    an = Field()
    judet = Field()
    nume = Field()
    url = Field()
    pozitia_pe_tara = Field()
    unitate_de_invatamant = Field()
    lb_romana_nota = Field()
    lb_romana_contestatie = Field()
    lb_romana_final = Field()
    matematica_nota = Field()
    matematica_contestatie = Field()
    matematica_final = Field()
    lb_materna = Field()
    lb_materna_nota = Field()
    lb_materna_contestatie = Field()
    lb_materna_final = Field()
    media = Field()
