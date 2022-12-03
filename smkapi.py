""" 
smkapi.py

Module that implements functions for accessing the SMK API developed by
Statens Museum for Kunst (SMK) to Wikimedia Commons 
using the pwikiibot framework as part of a collaboration between 
SMK and Wikimedia Denmark

For more details, refer to the project page on Commons:
https://commons.wikimedia.org/wiki/Commons:SMK_-_Statens_Museum_for_Kunst
"""

from dataclasses import dataclass
from typing import Any, Optional, List, TypeVar, Type, Callable, cast
from enum import Enum
from datetime import datetime
import dateutil.parser
import json
import requests
import pathlib
import smkitem

def get_smk_object(object_number):
    """
    Function that returns JSON given a SMK object number
    <object_number>::=<char>{<char>}
    """
    # url = 'https://api.smk.dk/api/v1/art/search/?keys=*&filters=%5Bobject_number%3D'+object_number+'%5D'
    url = 'https://api.smk.dk/api/v1/art/?object_number='+object_number

    smk_json=requests.get(url).text

    #data=json.loads(smk_json)
    
    return(smk_json)

# Get all wikidata items for SMK Wikidata object Q671384
#wikidata.GetInstitutionWikidataItems('Q671384', 'wikidata_smk.csv')
#TestSMKAPI()
#get_smk_object('KMS1')

def last_flagged(seq):
    """ Function that returns true if the list item the last item. """
    seq = iter(seq)
    a = next(seq)
    for b in seq:
        yield a, False
        a = b
    yield a, True        

def generate_smk_filter(smk_filter_list):
    smk_filter=""
    try:
        for filter,is_last in last_flagged(smk_filter_list):
            smk_filter=smk_filter+"%5B"+filter[0]+"%3A"+filter[1]+"%5D"
            if not is_last:
                smk_filter=smk_filter+","
    except:
        smk_filter=""

    return smk_filter

def get_smk_objects(smk_filter, offset, rows):
#    url='https://api.smk.dk/api/v1/art/search/?keys=*&offset='+str(offset)+'&rows='+str(rows)
    url='https://api.smk.dk/api/v1/art/search/?keys=*&filters=%5Bpublic_domain%3Atrue%5D,%5Bhas_image%3Atrue%5D&offset='+str(offset)+'&rows='+str(rows)
    #https://api.smk.dk/api/v1/art/search/?keys=*&filters=%5Bpublic_domain%3Atrue%5D,%5Bhas_image%3Atrue%5D,%5Bcreator_gender%3Akvinde%5D,%5Bcreator_nationality%3Adansk%5D&offset=0&rows=10
    url='https://api.smk.dk/api/v1/art/search/?keys=*&filters=%5Bpublic_domain%3Atrue%5D,%5Bhas_image%3Atrue%5D,%5Bcreator_gender%3Akvinde%5D,%5Bcreator_nationality%3Adansk&offset='+str(offset)+'&rows='+str(rows)
    url='https://api.smk.dk/api/v1/art/search/?keys=*'
    #url='https://api.smk.dk/api/v1/art/search/?keys=*&filters=%5Bcreator%3APiranesi%2C%20Giovanni%20Battista%5D&offset='+str(offset)+'&rows='+str(rows)
    if smk_filter!='':
        url=url+'&filters='+smk_filter
    url=url+'&offset='+str(offset)+'&rows='+str(rows)

    smk_json=requests.get(url).text
    #data=json.loads(requests.get(url).text)
    #data=json.loads(smk_json)
    
    #result = smkitem.smkitem_from_dict(json.loads(requests.get(url).text))

    return(smk_json)

def smk_to_commons_position(smk_position):
    """Function that strings defining a position used by SMK API to Wikimedia Commons strings
    Keyword arguments:
    smk_position -- the position code used by SMK API
        <smk_position>::={<char>} |
        <empty>
    
    Returns: 
    Mapped position code, empty if not mapped
        <iso_language_code>::={<char>} 
    """
    switcher = {
        "f.n.t.v.": "bottomleftcorner",
        "f.n.t.h.": "bottomrightcorner",
        "f.o.t.v.": "topleftcorner",
        "f.o.t.h.": "toprightcorner",
        "midtfor t.v.": "centerleft",
        "": ""
    }
    return switcher.get(smk_position.lower(), "smk_position:"+ smk_position+ "is not defined")

def smk_language_code_to_iso_code(smk_language_code):
    """Function that translates language identificers used by SMK API to ISO language codes
        Keyword arguments:
        smk_language_code -- the languge code used by SMK API
            <smk_language_code>::={<char>} |
            <empty>
     
        Returns: 
        Mapped ISO language code, empty if not mapped
            <iso_language_code>::=[<char>][<char>] |
            <empty>
    """
    switcher = {
        "dansk": "da",
        "eng": "en",
        "engelsk": "en",
        "italiensk": "it",
    }
    return switcher.get(smk_language_code.lower(), "")

def smk_danish_to_english(smk_danish):
    """Translates Danish terms used by SMK API to English.
    
    Keyword arguments:
        smk_danish -- the Dansih term used by SMK API
            <smk_danish>::= {<char>}
        returns -- Mapped English term, empty if not mapped
            <english>   ::= {<char>}
     """
    switcher = {
        "altertavle (maleri)": "altarpiece",
        "clairobscurtræsnit": "chiaroscuro woodcut",
        "akvarel": "water colour",
        "boghåndværk": "book craft",
        "collage": "collage",
        "dybtryk": "intaglio",
        "film/video/lyd/computer": "multimedia",
        "fotografi": "photograph",
        "fotogravure-heliogravure": "photo gravure",
        "fotoserigrafi": "screen printing",
        "gouache": "gouache painting",
        "installation": "installation art",
        "kobberstik": "etching",
        "maleri": "painting",
        "mezzotinte": "mezzotint",
        "objekt": "objects",
        "radering": "engraving",
        "skulptur": "sculpture",
        "tegning": "drawing",
        "træsnit": "woodcut",
        "blyant": "pencil",
        "video": "video",
    }
    ret_val = switcher.get(smk_danish.lower(), smk_danish) 

    return ret_val


def smk_nationality_to_wikidata_q(smk_nationality):
    """Translates SMK Nationalities used by SMK API to Wikidata Q-items.
    
    Keyword arguments:
        smk_nationality -- the Dansih name used for nationality by SMK API
            <smk_nationality>::= {<char>}
        returns -- Mapped Wikidata Q-number, empty if not mapped
            <english>   ::= {<char>}
     """
    switcher = {
        "Amerikansk": "Q30",
        "Argentinsk": "Q414",
        "Belgisk": "Q31",
        "Brasiliansk": "Q155",
        "Britisk": "Q145",
        "Canadisk": "Q16",
        "Dansk": "Q756617",
        "Engelsk": "Q21",
        "Finsk": "Q33",
        "Flamsk": "Q234",
        "Fransk": "Q142",
        "Færøsk": "Q4628",
        "Græsk": "Q41",
        "Grønlandsk": "Q223",
        "Hollandsk": "Q102911",
        "Indisk": "Q102911",
        "Irsk": "Q22890",
        "Islandsk": "Q189",
        "Israelsk": "Q801",
        "Italiensk": "Q38",
        "Japansk": "Q17",
        "Kroatisk": "Q224",
        "litauisk": "Q37",
        "Mexicansk": "Q96",
        "Nederlandsk": "Q55",
        "Norsk": "Q55",
        "Polsk": "Q36",
        "Portugisisk": "Q45",
        "Rumænsk": "Q218",
        "Russisk": "Q159",
        "Schweizisk": "Q39",
        "Serbisk": "Q403",
        "Skotsk": "Q22",
        "Slovensk": "Q215",
        "Spansk": "Q29",
        "Svensk": "Q29",
        "Tjekkisk": "Q29",
        "Tyrkisk": "Q29",
        "Tysk": "Q183",
        "Ungarsk": "Q28",
        "Venezuelansk": "Q717",
        "Østrigsk": "Q40",
    }
    wikidata_q = switcher.get(smk_nationality.lower(), "") 

    return wikidata_q

def smk_nationality_to_english(smk_nationality):
    """Translates SMK Nationalities used by SMK API to Wikidata Q-items.
    
    Keyword arguments:
        smk_nationality -- the Dansih name used for nationality by SMK API
            <smk_nationality>::= {<char>}
        returns -- Mapped Wikidata Q-number, empty if not mapped
            <english>   ::= {<char>}
     """
    switcher = {
        "amerikansk": "American",
        "argentinsk": "Argentine",
        "belgisk": "Belgian",
        "brasiliansk": "Brazilian",
        "britisk": "British",
        "canadisk": "Canadian",
        "dansk": "Danish",
        "engelsk": "English",
        "finsk": "Finish",
        "flamsk": "Flemish",
        "fransk": "French",
        "færøsk": "Faroese",
        "græsk": "Greek",
        "grønlandsk": "Greenlandish",
        "gollandsk": "Dutch",
        "indisk": "Indian",
        "irsk": "Irish",
        "islandsk": "Icelandic",
        "israelsk": "Israeli",
        "italiensk": "Italian",
        "japansk": "Japanase",
        "kroatisk": "Croatian",
        "litauisk": "Lithuanian",
        "mexicansk": "Mexican",
        "nederlandsk": "Nederlandish",
        "norsk": "Norwegian",
        "polsk": "Polish",
        "portugisisk": "Portugeese",
        "rumænsk": "Romanian",
        "russisk": "Rissian",
        "schweizisk": "Swiss",
        "serbisk": "Serbian",
        "skotsk": "Scotish",
        "slovensk": "Slovenian",
        "spansk": "Spanish",
        "svensk": "Swedish",
        "tjekkisk": "Czeck",
        "tyrkisk": "Turkish",
        "tysk": "German",
        "ungarsk": "Hungarian",
        "venezuelansk": "Venezuelean",
        "østrigsk": "Austrian",
    }
    english = switcher.get(smk_nationality.lower(), "") 

    return english

def smk_gender_to_wikidata_q(smk_gender):
    """Function that translates gender identificers used by SMK API to ISO language codes
        Keyword arguments:
        smk_gender -- the gender code used by SMK API
            <smk_gender>::={<char>} |
            <empty>
     
        Returns: 
        Mapped gender code, empty if not mapped
            <wikidata_q_code>::="Q"<digit>{<digit>}* |
            <empty>
    """
    switcher = {
        "MALE": "Q6581097",
        "FEMALE": "Q6581072",
        "UNKNOWN": '"somevalue"',
        }
    return switcher.get(smk_gender, "")

def smk_danish_to_wikidata_q(smk_danish):
    """Translates SMK Danish terms used by SMK API to Wikidata Q-items.
    
    Keyword arguments:
        smk_danish -- the Dansih term used by SMK API
            <smk_danish>::= {<char>}
        returns -- Mapped Wikidata Q-number, empty if not mapped
            <q-item>   ::= Q<digit>{<digit>}*
     """
    switcher = {
        "altertavle (maleri)": "Q15711026",
        "clairobscurtræsnit:": "Q1027974",
        "akvarel": "Q50030",
        "boghåndværk": "Q4583685",
        "collage": "Q22669857",
        "dybtryk:": "Q12309090",
        "film/video/lyd/computer": "Q131765",
        "fotografi": "Q125191",
        "fotogravure-heliogravure:": "Q23657361",
        "fotoserigrafi": "Q187791",
        "gouache:": "Q21281546",
        "installation:": "Q20437094",
        "kobberstik": "Q18218093",
        "maleri": "Q3305213",
        "mezzotinte": "Q21647744",
        "objekt": "Q488383",
        "radering": "Q18218093",
        "skulptur": "Q860861",
        "tegning": "Q93184",
        "træsnit": "Q18219090",
        "blyant": "Q85621166",
        "video:": "Q20742776",    }
    wikidata_q = switcher.get(smk_danish.lower(), "") 

    return wikidata_q

def smk_documentation_to_commons_citation(smk_documentation):
    """Formats a smk_documentation node from the SMK API to a Wikimedia Commons citation template.
    
    Example:
    citation = smk_documentation_to_commons_citation("")
    
    Keyword arguments:
    smk_documentation -- the documentation node has at least these keys:
        <title>     ::= {<char>}
        <author>    ::= {<char>}
        <note>      ::= {<char>}
        <shelfmark> ::= {<char>}
        <year_of_publication> 
                    ::= [<number>][<number>][<number>][<number>]
    
    Returns -- A commons citation template formatted like this:
        <citation>  ::= "{{Citation" |
            ["|title="<title>] |
            ["|author="<author>] |
            ["|others="<notes>] |
            ["|id="<shelfmark>] |
            ["|year="<year_of_publication>] |
            "}}" |
            <empty>
        Example: 
            {{Citation
                |title=Title
                |author=Author
                |others=Notes
                |id=Shelfmark>
            }}
    """
    commons_cite = ''
    title = ''
    author = ''
    notes = ''
    shelfmark = ''
    year_of_publication = ''
    if smk_documentation.get('title') is not None:
        title = str(smk_documentation.get('title'))
        if title == 'None':
            title = ''
    if smk_documentation.get('author') is not None:
        author = str(smk_documentation.get('author')) 
        if author == 'None':
            author = ''
    if smk_documentation.get('notes') is not None:
        notes = str(smk_documentation.get('notes'))
        if notes == 'None':
            notes = ''
    if smk_documentation.get('shelfmark') is not None:
        shelfmark = str(smk_documentation.get('shelfmark'))
        if shelfmark == 'None':
            shelfmark = ''
    if smk_documentation.get('year_of_publication') is not None:
        year_of_publication = str(smk_documentation.get('year_of_publication'))
        if year_of_publication == 'None':
            year_of_publication = ''
    if title != '' or author != '' or notes != '' or shelfmark != '' or year_of_publication != '':
        commons_cite = '{{citation'
        if title != '':
            commons_cite = commons_cite + '|title=' + title
        if author != '':
            commons_cite = commons_cite + '|author=' + author
        if notes != '':
            commons_cite = commons_cite + '|others=' + notes
        if shelfmark != '':
            commons_cite = commons_cite + '|id=' + shelfmark
        if year_of_publication != '':
            commons_cite = commons_cite + '|year=' + year_of_publication
        else:
            commons_cite = commons_cite + '|date=date unspecfied'
        commons_cite = commons_cite + '}}'
    return commons_cite