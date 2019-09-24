# smkbatch
#
# Functions for SMK Batch Upload
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
import commons
import wikidata
import os
import pywikibot
from pywikibot import pagegenerators as pg
import logging

def TestSMKAPI():
    #url = [ filename ]
    #keepFilename = False        #set to True to skip double-checking/editing destination filename
    keepFilename = True        #set to True to skip double-checking/editing destination filename
    #verifyDescription = True    #set to False to skip double-checking/editing description => change to bot-mode
    verifyDescription = False    #set to False to skip double-checking/editing description => change to bot-mode
    #targetSite = pywikibot.Site('beta', 'commons')

    #bot = UploadRobot(url, description=description, useFilename=pagetitle, keepFilename=keepFilename, verifyDescription=verifyDescription, targetSite=targetSite)
    #bot.run()

    # Get JSON from the SMK API
    #json_string = json.loads(requests.get("https://api.smk.dk/api/v1/art/search/?keys=*&filters=%5Bpublic_domain%3Atrue%5D,%5Bhas_image%3Atrue%5D&offset=0&rows=10").text)
    #json_string = json.loads(requests.get("https://api.smk.dk/api/v1/art/search/?keys=*&filters=%5Bobject_number%3AKMS1%5D").text)

    #THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    #my_file = os.path.join(THIS_FOLDER, 'smkitems.json')

    #json_file = open(my_file)
    #json_string = json.load(json_file)

    # Map to obejct model
    #smk_items = smkitem.empty_from_dict(json_string)

    # Add categories
    categories  = """[[Category:Wiki Labs Kultur]]
    [[Category:Paintings in Statens Museum for Kunst]]"""

    # Iterate over Items
    # for item in smk_items.items:
    
    #     # Check for image
    #     if item.has_image: 
    #         filename=item.image_native
    #         path=pathlib.Path(filename)
            
    #         # Generate page title
    #         pagetitle='SMK-' + item.id + '-' + item.object_number + ':' + item.titles[0].title + path.suffix

    #         # Generate description
    #         desc = ''
    #         if item.content_description is not None:
    #             for line in item.content_description:
    #                 desc=desc+line
            
    #         # Generate date
    #         production_date = ''
    #         for date in item.production_date:
    #             production_date = production_date+date.start.strftime("%Y-%m-%d")+' - '+date.end.strftime("%Y-%m-%d")+'\n'  


    #         #complete_artwork_desc_and_upload(filename, pagetitle, desc, production_date, categories)

    #         # Generate artwork template
    #         artwork = commons.ArtworkTemplate(artist = '',
    #             author = '',
    #             title = '',
    #             desc = desc,
    #             depicted_people = '',
    #             date = production_date,
    #             medium = '',
    #             dimensions = '',
    #             institution = '',
    #             department = '',
    #             place_of_discovery = '',
    #             object_history = '', 
    #             exhibition_history = '',
    #             credit_line = '',
    #             inscriptions = '',
    #             notes = '',
    #             accession_number = item.object_number,
    #             place_of_creation = '',
    #             source = '',
    #             permission = '',
    #             other_versions = '',
    #             references = '',
    #             depicted_place = '',
    #             wikidata = '',
    #             categories = categories)

    #             #artwork.GenerateWikiText()

    #         print ('id           =' + item.id)
    #         print ('object_number=' + item.object_number)
    #         print ('image_native =' + item.image_native)
    #         print (artwork.wikitext)

# Get all wikidata items for SMK Wikidata object Q671384
wikidata.GetInstitutionWikidataItems('Q671384', 'wikidata_smk')
#TestSMKAPI()
#get_smk_object('KMS1')