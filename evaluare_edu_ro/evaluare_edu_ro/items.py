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


class AdmitereEduRoItem(Item):
    nume = Field()
    scoala_de_provenienta = Field()
    judet = Field()
    media_la_admitere = Field()
    media_en_tsu = Field()
    media_de_absolvire = Field()
    nota_lb_romana = Field()
    nota_matematica = Field()
    optiunea_3 = Field()
    nota_optiunea_3 = Field()
    limba_materna = Field()
    nota_lb_materna = Field()
    liceu_repartizat = Field()
    tip_liceu = Field()
    specializare = Field()
    specializare_lb = Field()


class LiceuEduRoItem(Item):
    nume = Field()
    an = Field()
    tip = Field()
    judet = Field()
    localitate = Field()
    sectorul = Field()
    adresa = Field()
    telefon = Field()
    fax = Field()
    mediu = Field()
    specializari = Field()
    cod_liceu = Field()

class SpecializareLiceuItem(Item):
    cod = Field()
    nivel = Field()
    profil = Field()
    denumire = Field()
    candidati_repartizati = Field()
    nr_locuri = Field()
    forma_invatamant = Field()
    limba_predare = Field()
    bilingv = Field()
    filiera = Field()
    mediul = Field()
    ultima_medie = Field()
    ultima_medie_precedenta = Field()


class ScoalaItem(Item):
    an = Field()
    judet = Field()
    cod = Field()
    nume = Field()
    nr_candidati = Field()
    nr_repartizati = Field()
    nr_nerepartizati = Field()
    mediu = Field()
    adresa = Field()
    sector = Field()
    telefon = Field()
    fax = Field()
    e_mail = Field()
    tip = Field()