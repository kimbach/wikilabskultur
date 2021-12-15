# commons - module than implements helper classes for Wikimedia Commons
#
# Artwork class encapsulates the wikimedia commons temlate Artwork
#  
# This code parses date/times, so please
#
#     pip install python-dateutil
#

from dataclasses import dataclass
from typing import Any, Optional, List, TypeVar, Type, Callable, cast
from enum import Enum
from datetime import datetime
import dateutil.parser
from abc import ABCMeta, abstractmethod
import hashlib
import json
import requests

@dataclass
class BaseTemplate(metaclass=ABCMeta):
    @abstractmethod
    def GenerateWikiText(self):
        #complete this once if applies to all files
        pass

@dataclass
class ArtworkTemplate(BaseTemplate):
    artist: str
    nationality: str
    author: str
    title: str
    desc: str
    depicted_people: str
    date: str
    medium: str
    dimensions: str
    institution: str
    department: str
    place_of_discovery: str
    object_history: str 
    exhibition_history: str
    credit_line: str
    inscriptions: str
    notes: str
    accession_number: str
    place_of_creation: str
    source: str
    permission: str
    other_versions: str
    references: str
    depicted_place: str
    wikidata: str
    categories: str
    orientation: str
    wikitext: str
    csvline: str
    csvheader: str
    imageurl: str
    image_height: str
    image_width: str
    object_type: str
    location: str

    def __init__(self, 
        artist = '',
        nationality = '',
        author = '',
        title = '',
        desc = '',
        depicted_people = '',
        date = '',
        medium = '',
        dimensions = '',
        institution = '',
        department = '',
        place_of_discovery = '',
        object_history = '', 
        exhibition_history = '',
        credit_line = '',
        inscriptions = '',
        notes = '',
        accession_number = '',
        place_of_creation = '',
        source = '',
        permission = '',
        other_versions = '',
        references = '',
        depicted_place = '',
        wikidata = '',
        categories = '',
        imageurl = '',
        image_height = '',
        image_width = '',
        object_type = '',
        location = ''):

        self.artist = artist.rstrip('\n')
        self.nationality = nationality.rstrip('\n')
        self.author = author.rstrip('\n')
        self.title = title.rstrip('\n')
        self.depicted_people = depicted_people.rstrip('\n')
        self.desc = desc.rstrip('\n')
        self.date = date.rstrip('\n')
        self.medium = medium.rstrip('\n')
        self.dimensions = dimensions.rstrip('\n')
        self.institution = institution.rstrip('\n')
        self.department = department.rstrip('\n')
        self.place_of_discovery = place_of_discovery.rstrip('\n')
        self.object_history = object_history.rstrip('\n')
        self.exhibition_history = exhibition_history.rstrip('\n')
        self.credit_line = credit_line.rstrip('\n')
        self.inscriptions = inscriptions.rstrip('\n')
        self.notes = notes.rstrip('\n')
        self.accession_number = accession_number.rstrip('\n')
        self.place_of_creation = place_of_creation.rstrip('\n')
        self.source = source.rstrip('\n')
        self.permission = permission.rstrip('\n')
        self.other_versions = other_versions.rstrip('\n')
        self.references = references.rstrip('\n')
        self.depicted_place = depicted_place.rstrip('\n')
        self.wikidata = wikidata.rstrip('\n')
        self.categories = categories.rstrip('\n')
        self.image_height = image_height.rstrip('\n')
        self.image_width = image_width.rstrip('\n')
        self.imageurl = imageurl.rstrip('\n')
        self.object_type = object_type.rstrip('\n')
        self.location = location.rstrip('\n')
        self.GenerateWikiText()

    def GenerateWikiText(self):
        #complete this once if applies to all files
        if self.wikidata != '':
            self.artist = ''

        self.wikitext = u"""{{Artwork
    |artist             = """ + str(self.artist) + """
    |author             = """ + str(self.author) + """
    |title              = """ + str(self.title) + """
    |description        = """ + str(self.desc) + """
    |depicted people    = """ + str(self.depicted_people) + """
    |date               = """ + str(self.date) + """
    |medium             = """ + str(self.medium) + """
    |dimensions         = """ + str(self.dimensions) + """
    |institution        = """ + str(self.institution) + """
    |department         = """ + str(self.department) + """
    |place of discovery = """ + str(self.place_of_discovery) + """
    |object history     = """ + str(self.object_history) + """ 
    |exhibition history = """ + str(self.exhibition_history) + """
    |credit line        = """ + str(self.credit_line) + """
    |inscriptions       = """ + str(self.inscriptions) + """
    |notes              = """ + str(self.notes) + """
    |accession number   = """ + str(self.accession_number) + """
    |place of creation  = """ + str(self.place_of_creation) + """
    |source             = """ + str(self.source) + """
    |permission         = """ + str(self.permission) + """
    |other_versions     = """ + str(self.other_versions) + """
    |references         = """ + str(self.references) + """
    |depicted place     = """ + str(self.depicted_place) + """
    |object type        = """ + str(self.object_type) + """
    |location           = """ + str(self.location) + """
    """
        if self.wikidata != '':
            self.wikitext = self.wikitext + """
    |wikidata           = """ + self.wikidata + """
    """

        self.wikitext = self.wikitext + """
}}
    """

    def GenerateCSVLine(self, csvdelim=';'):
        #complete this once if applies to all files
        self.csvline = ''
        self.csvline = self.csvline + self.artist.replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + self.nationality.replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + self.author.replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + self.title.replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + self.desc.replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + self.depicted_people.replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + self.date.replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + self.medium.replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + self.dimensions.replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + self.institution.replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + self.department.replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + self.place_of_discovery.replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + self.object_history.replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + self.exhibition_history.replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + self.credit_line.replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + self.inscriptions.replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + self.notes.replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + self.accession_number.replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + self.place_of_creation.replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + self.source.replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + self.permission.replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + self.other_versions.replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + self.references.replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + self.depicted_place.replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + self.categories.replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + self.wikidata.replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + self.image_height.replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + self.image_width.replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + self.imageurl 
        self.csvline = self.csvline + self.object_type 
        self.csvline = self.csvline + self.location 
    
        return self.csvline

    def GenerateCSVHeader(self, csvdelim=';'):
        #complete this once if applies to all files

        self.csvheader = 'artist' + csvdelim + \
          'nationality' + csvdelim + \
          'author' + csvdelim + \
          'title' + csvdelim + \
          'description' + csvdelim + \
          'depicted_people' + csvdelim + \
          'date' + csvdelim + \
          'medium' + csvdelim + \
          'dimensions' + csvdelim + \
          'institution' + csvdelim + \
          'department' + csvdelim + \
          'place_of_discovery' + csvdelim + \
          'object_history' + csvdelim + \
          'exhibition_history' + csvdelim + \
          'credit_line' + csvdelim + \
          'inscriptions' + csvdelim + \
          'notes' + csvdelim + \
          'accession_number' + csvdelim + \
          'place_of_creation' + csvdelim + \
          'source' + csvdelim + \
          'permission' + csvdelim + \
          'other_versions' + csvdelim + \
          'references' + csvdelim + \
          'depicted_place' + csvdelim + \
          'categories' + csvdelim + \
          'wikidata' + csvdelim + \
          'image_height' + csvdelim + \
          'image_width' + csvdelim + \
          'imageurl' + csvdelim + \
          'object_type' + csvdelim + \
          'location'
    
        return self.csvheader

def check_image_hash(image_filename):
    file = image_filename # Location of the file (can be set a different way)
    BLOCK_SIZE = 65536 # The size of each read from the file

    file_hash = hashlib.sha1() # Create the hash object, can use something other than `.sha256()` if you wish
    with open(file, 'rb') as f: # Open the file to read it's bytes
        fb = f.read(BLOCK_SIZE) # Read from the file. Take in the amount declared above
        while len(fb) > 0: # While there is still data being read from the file
            file_hash.update(fb) # Update the hash
            fb = f.read(BLOCK_SIZE) # Read the next block from the file

    print (file_hash.hexdigest()) # Get the hexadecimal digest of the hash    
    url= "https://commons.wikimedia.org/w/api.php?action=query&format=json&list=allimages&prop=imageinfo&aisha1=" + file_hash.hexdigest()
    data = json.loads(requests.get(url).text)
    if len(data['query']['allimages']) != 0:
        # file hash found
        retval=True 
    else:
        retval=False 
    return(retval)

# -*- coding: utf-8  -*-

import sys

import pywikibot
from pywikibot.specialbots import UploadRobot

def complete_desc_and_upload(filename, pagetitle, desc, date, categories):
    #complete this once if applies to all files

    description = u"""{{Artwork
    |artist             = 
    |author             = 
    |title              = {{title|Skt. Victor af Siena|lang=da}}
    |description        = * {{da|Det synes vanskeligt at bestemme helgenens navn, S. Victor, S. Galgano, S. Ansanu oa. er bragt i forslag. Marianne Lonjon foreslår i brev 10 febr. 1984, at helgenen er Sankt Victor af Siena og mener at triptykket har været bestemt til den hellige Victors kapel i Siena.}}
    |depicted people    = 
    |date               = 1348-1352
    |medium             = Tempera på træ. Guldgrund
    |dimensions         = 
    |institution        = {{Institution:Statens Museum for Kunst, Copenhagen}}
    |department         = 
    |place of discovery = 
    |object history     = * {{da|- William Young Ottleys - Bromleys Samling - Lord Ashburtons Samling - Grev Avoglis Samling, - H.Heilbuths Samling (udstillet med denne i Kunstmuseet Efteråret 1920) - Ehrich Galleries, New York. - Købt med pendanten (KMS3624) for 30.000kr af Dansk Kunstmuseumsforening Placeringshistorie: - 1966, maj: Kunstindustrimuseet - 1969, 28. aug.: Retur Sølvgade}}
* {{ProvenanceEvent|date=1923-12-31|type=acquisition|newowner=[[Statens Museum for Kunst]]}} 
    |exhibition history = * {{Temporary Exhibition |name=100 Mesterværker |institution= |place= Sølvgade |begin=1996-06-23 |end=1996-08-04}}
    |credit line        = 
    |inscriptions       = 
    |notes              = * {{da|Tidligere tilskrevet Simone Martini}}
* {{da|Tidligere tilskrevet Lippo Memmi}}
* {{da|Katalognumre: - Kat. 1946 nr. 441}}
* {{da|Santa Corona og Skt. Victor af SienaLegenden fortæller, at den kun 16 år gamle Santa Corona i et syn så en engel stige ned fra himlen med to kroner, en mere beskeden til hende selv og en mere kostbar til Skt. Victor, som hun for sin kristne tros skyld skulle lide martyrdøden sammen med.Skildringen af de to helgenerKunstneren har skildret hende med den lille krone på hovedet og den store elegant støttet med venstre hånds fingerspidser. I sin højre hånd holder hun ligesom Skt. Victor martyriets trofæ, et par palmegrene. Skt. Victor holder desuden en olivengren, symbolet for den sejr, som Siena vandt over Montepulciano og Orvieto i 1229 på det, der senere blev Skt. Victors dag.Eksempler på den sienesiske gotikTavlerne var oprindeligt sidefløje til et hovedstykke med hyrdernes tilbedelse malet af Bartolomeo Bulgarini (1300/1310-1378). De er meget sjældne og fine eksempler på den sienesiske gotiks særlige lineære og farvestrålende dekorative stil, der står i kontrast til den rivaliserende florentinske skole, som mere betoner massen og tyngden.Storstilet udsmykning af domkirkenAltertavlen blev lavet omkring eller umiddelbart efter peståret 1348, som mere end decimerede Sienas befolkning. Skt. Viktor-altertavlen satte punktum for en storstilet udsmykning af byens domkirke, en udsmykning, som også omfattede den altertavle, som Ambrogio Lorenzettis (før 1317 - ca.1384) Johannes Døberen var del af. Highlights 2005, Eva de la Fuente Pedersen.}}
    |accession number   = KMS3625
    |place of creation  = 
    |source             = * {{SMK API|KMS3625}}
* {{SMK Open|KMS3625}}
* [https://api.smk.dk/api/v1/download/W3siaW1nX3VybCI6Imh0dHBzOi8vaWlwLnNtay5kay9paWlmL2pwMi9LTVMzNjI1LnRpZi5yZWNvbnN0cnVjdGVkLnRpZi5qcDIvZnVsbC9mdWxsLzAvbmF0aXZlLmpwZyIsInB1YmxpY19kb21haW4iOnRydWUsIm9iamVjdF9udW1iZXIiOiJLTVMzNjI1IiwibnVtIjoiIn1d/KMS3625.jpg image]
    |permission         = {{Licensed-PD-Art|PD-old|Cc-zero}}
	{{Statens Museum for Kunst collaboration project}}
    |other_versions     = 
    |references         = *{{citation|title=Italiensk kunst og kunstindustri|author=Erik Zahle|others=6, afb. 4, 78f|id=11782|year=1934}}
*{{citation|title=Pitture italiane del rinascimento: catalogo dei principali artisti e delle loro opere con un indice dei luoghi|author=Bernhard (Bernard) Berenson|others=309|id=13538|year=1936}}
*{{citation|title=Fire italienske billeder i dansk eje|author=Erik Moltesen|others=86ff|id=15129|year=1925}}
*{{citation|title=En samling af ældre malerkunst: udstillet i museet i efteraaret 1920|author=Karl Madsen|others=p. 112 (afb.), 114|id=15158|year=1920}}
*{{citation|title=Siena and the Virgin: art and politics in a late medieval city state|author=Diana Norman|others=p. 68, 73, 74, 79, 80 og 84, samt note 12, p. 122. Afb. p. 73 (Forsøg på rekonstruktion af panelets oprindelige placering som alterfløj, samt oplysninger om det ikonografiske program.)|id=2000-033|year=1999}}
*{{citation|title=Simone Martini e l'Annunciazione degli Uffizi|author=Alessandro Cecchi|others=pp. 38ff, ill. fig. 5 p. 43 + fig. 8 p. 45 (rekonstruktion af panelets placering i oprindelig altertavle m.v.).|id=2002-071|year=2001}}
*{{citation|title=A program completed: the identification of the San Vittorio altarpiece|author=Kavin M. Frederick|others=p.56-63, ill. (vedr. forslag til evt. komposition for et middelfelt mellem de to helgener, de tilsammen udgjorde altertavle i S.Vittorio-kapellet i Katedralen i Siena) (artiklen er en fortsættelse af den i K.M.Friedrick, A Program of Alterpieces for the Siena Cathedral. KMS' maleri nævnes ikke i denne sidste artikel, men altercyklen præsenteret - særtryk i biblioteket.)|id=2002-492|year=1983, 1985}}
*{{citation|title=Lippo Memmi's Helgen og Helgeninde|author=Erik Zahle|others=p.282f (om billedets tidligere historie og ældre litteratur)|id=2002-514}}
*{{citation|title=SMK highlights: Statens Museum for Kunst|author=Sven Bjerkhof|others=omt. og afb. p. 18|id=2005-071|year=2005}}
*{{citation|title=Italian paintings and sculpture in Denmark|author=Harald Olsen|others=p.22, p.75, afb. planche II, a (Tilskrevet Palazo Venezia Madonna-mesteren)|id=28349|year=1961}}
*{{citation|title=Catalogue of a collection of paintings|author=Karl Madsen|others=nr. 2|id=6834}}
*{{citation|title=Statens Museum for Kunst: 1827-1952|author=Villads Villadsen|others=afb. (s/h) p.222|id=98-419|year=1998}}
*{{citation|title=The development of the Italian schools of painting|author=Raimond van Marle|others=vol. II (1924): 292ff, tilskrevet Barna da Siena|id=C 3075:1-19 it|year=1923-1938}}
*{{citation|title=Maletekniske undersøgelser af to helgenbilleder fra Skt. Victor-altertavlen i Sienas domkirke|author=Troels Filtenborg|others=omt. p. 83ff, ill. p. 84, samt flere detaljefotografier|year=2006}}
*{{citation|title=Tuscan Primitives in London Sales, 1801-1837|author=Dorothy Lygon|others=p. 113, 114, 115}}
*{{citation|title=Iconography of the Saints in Tuscan Painting|author=George Kaftal|others=fig. 1137: S. Vittore de Siena|year=1952}}
*{{citation|title=100 mesterværker|author=Eva Friis|others=p.30, afb. p.31|id=k1996-233|year=1996}}
    |depicted place     = 
    |object type        = Altarpiece
    |location           = Sal 201B
    
    |wikidata           = Q48453396
    
}}
    

[[Category:Images released under the CC0 1.0 Universal license by Statens Museum for Kunst]]
[[Category:Images from the partnership with Statens Museum for Kunst]]
[[Category:Altarpieces in Statens Museum for Kunst]]

"""
    url = [ filename ]
    #keepFilename = False        #set to True to skip double-checking/editing destination filename
    keepFilename = True        #set to True to skip double-checking/editing destination filename
    #verifyDescription = True    #set to False to skip double-checking/editing description => change to bot-mode
    verifyDescription = False    #set to False to skip double-checking/editing description => change to bot-mode
    #targetSite = pywikibot.Site('commons', 'commons')
    #targetSite = pywikibot.Site(fam='commons',code='commons', user='Kim Bach', sysop='Kim Bach')
    try:
        targetSite = pywikibot.Site()
    except Exception as e:
        print(str(e))

    print(targetSite)
    targetSite = pywikibot.Site('commons', 'commons')

    bot = UploadRobot(url, description=description, useFilename=pagetitle, keepFilename=keepFilename, verifyDescription=verifyDescription, targetSite=targetSite, summary='Created artwork')
    bot.run()

#    page = pywikibot.Page(targetSite, 'File:' + filename)
#    page = pywikibot.Page(targetSite, 'File:' + filename)
#    print(page.text)
#    page.text = description
#    page.save('Replacing description')  # Saves the page

def complete_artwork_desc_and_upload(filename, pagetitle, desc, date, categories):
    #complete this once if applies to all files

    description = u"""{{Artwork
|Description    = {{en|1=""" + desc + """}}
|Source         = [[Statens Museeum for Kunst]]
|Author         = 
|Date           = """ + date + """
|Permission     = 
|other_versions = 
}}
=={{int:license-header}}==
{{PD-old-70}}

""" + categories + """
"""
    url = [ filename ]
    #keepFilename = False        #set to True to skip double-checking/editing destination filename
    keepFilename = True        #set to True to skip double-checking/editing destination filename
    #verifyDescription = True    #set to False to skip double-checking/editing description => change to bot-mode
    verifyDescription = False    #set to False to skip double-checking/editing description => change to bot-mode
    targetSite = pywikibot.Site(code='commons', fam='commons', user='Kim Bach')
    
    #bot = UploadRobot(url, description=description, useFilename=pagetitle, keepFilename=keepFilename, verifyDescription=verifyDescription, targetSite=targetSite)
    #bot.run()

#    page = pywikibot.Page(targetSite, 'File:' + filename)
    page = pywikibot.Page(targetSite, 'File:' + filename)
#    print(page.text)
    #page.text = description
    #page.save('Replacing description')  # Saves the page

def UploadTest():
    #list each file here
    
    filename    = """https://iip.smk.dk/iiif/jp2/KMS1.tif.reconstructed.tif.jp2/full/full/0/native.jpg"""
    filename    = """KMS1.tif.reconstructed.tif.jpg"""
    filename    = "./downloads/Mesteren for Palazzo Venezia Madonna, Skt. Victor af Siena, 1348-1352, KMS3625, Statens Museum for Kunst.jpg"
    pagetitle   = "Mesteren for Palazzo Venezia Madonna, Skt. Victor af Siena, 1348-1352, KMS3625, Statens Museum for Kunst.jpg"
    desc        = """The Heart Of Wiki Labs Kultur - Updated Image"""
    date        = "2016-10-14 22:06"
    date        = "2019-09-10 19:00"
    categories  = """[[Category:Wiki Labs Test]]"""
    categories  = """[[Category:Wiki Labs Test]]"""
    complete_artwork_desc_and_upload(filename, pagetitle, desc, date, categories)


    #sample with:  - local file name identical to file name at Commons
    #              - date as previous file
    #              - less quotes (no CR or " in fields)
    #filename   = "testimage-2.jpg"
    #pagetitle  = filename
    #desc       = "Mount St Helens as seen from ... at sunset"
    #categories = "[[Category:Locality]] [[Category:Theme]] [[Category:View type]] [[Category:Feature1]] [[Category:Feature2]]"
    #complete_desc_and_upload(filename, pagetitle, desc, date, categories)
   

#if __name__ == "__main__":
#    try:
#        main(sys.argv[1:])
#    finally:
#        pywikibot.stopme()
