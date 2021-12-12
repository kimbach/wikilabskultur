# smkapi
#
# Function for SMK API
#
# This code parses date/times, so please
#
#     pip install python-dateutil
#
# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = empty_from_dict(json.loads(json_string))

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
    # Function that returns JSON given a SMK object number
    # <object_number>::=
    # url = 'https://api.smk.dk/api/v1/art/search/?keys=*&filters=%5Bobject_number%3D'+object_number+'%5D'
    url = 'https://api.smk.dk/api/v1/art/?object_number='+object_number
    data = json.loads(requests.get(url).text)
    return(data)

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
    for filter,is_last in last_flagged(smk_filter_list):
        smk_filter=smk_filter+"%5B"+filter[0]+"%3A"+filter[1]+"%5D"
        if not is_last:
            smk_filter=smk_filter+","
    return smk_filter

def get_smk_objects(smk_filter, offset, rows):
#    url='https://api.smk.dk/api/v1/art/search/?keys=*&offset='+str(offset)+'&rows='+str(rows)
    url='https://api.smk.dk/api/v1/art/search/?keys=*&filters=%5Bpublic_domain%3Atrue%5D,%5Bhas_image%3Atrue%5D&offset='+str(offset)+'&rows='+str(rows)
    #https://api.smk.dk/api/v1/art/search/?keys=*&filters=%5Bpublic_domain%3Atrue%5D,%5Bhas_image%3Atrue%5D,%5Bcreator_gender%3Akvinde%5D,%5Bcreator_nationality%3Adansk%5D&offset=0&rows=10
    url='https://api.smk.dk/api/v1/art/search/?keys=*&filters=%5Bpublic_domain%3Atrue%5D,%5Bhas_image%3Atrue%5D,%5Bcreator_gender%3Akvinde%5D,%5Bcreator_nationality%3Adansk&offset='+str(offset)+'&rows='+str(rows)
    url='https://api.smk.dk/api/v1/art/search/?keys=*'
    if smk_filter!='':
        url=url+'&filters='+smk_filter
    url=url+'&offset='+str(offset)+'&rows='+str(rows)
    data=json.loads(requests.get(url).text)
    return(data)

def smk_to_commons_position(smk_position):
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
        "clairobscurtræsnit": "clair obscur woodcut",
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
        "video": "video",
    }
    ret_val = switcher.get(smk_danish.lower(), smk_danish) 

    return ret_val

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
        commons_cite = commons_cite + '}}'
    return commons_cite